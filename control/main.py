import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from pyit2fls import (
    IT2FLS, IT2FS, trapezoid_mf, tri_mf, min_t_norm, max_s_norm
)

# --- 1. CZĘŚĆ TN (LOGIKA STEROWNIKA) ---
def create_navigation_controller():
    system = IT2FLS()

    # Domeny
    speed_dom = np.linspace(0, 50, 100)
    noise_dom = np.linspace(40, 100, 100)
    vol_dom = np.linspace(0, 100, 100)

    # ZMIENNE WEJŚCIOWE (TYPE-2 SETS)
    # 1. Prędkość (Speed)
    # Low: Rozciągnięty koniec LMF do 18
    speed_low = IT2FS(speed_dom, 
        trapezoid_mf, [0.0, 0.001, 10, 22, 1.0],  # UMF
        trapezoid_mf, [0.0, 0.001, 12, 18, 1.0]   # LMF
    )
    # Med: Startuje wcześniej (8/12) i kończy później (32/36)
    speed_med = IT2FS(speed_dom, 
        trapezoid_mf, [8, 15, 25, 36, 1.0],       # UMF
        trapezoid_mf, [12, 17, 23, 32, 1.0]       # LMF
    )
    # High: Startuje dużo wcześniej (22/25), żeby mocno wejść na Med
    speed_high = IT2FS(speed_dom, 
        trapezoid_mf, [22, 32, 49.9, 50, 1.0],    # UMF
        trapezoid_mf, [25, 35, 49.9, 50, 1.0]     # LMF (Start 25 vs Med Koniec 32 -> 7 jednostek zakładki!)
    )

    # 2. Hałas (Noise)
    # Quiet: Rozciągnięty
    noise_quiet = IT2FS(noise_dom, 
        trapezoid_mf, [40, 40.001, 55, 68, 1.0], 
        trapezoid_mf, [40, 40.001, 58, 64, 1.0]
    )
    # Med: Szeroki zakres, mocne pokrycie
    noise_med = IT2FS(noise_dom, 
        trapezoid_mf, [50, 62, 72, 85, 1.0],      # UMF
        trapezoid_mf, [55, 64, 70, 80, 1.0]       # LMF
    )
    # Loud: Startuje wcześniej (70/75)
    noise_loud = IT2FS(noise_dom, 
        trapezoid_mf, [70, 85, 99.9, 100, 1.0],   # UMF
        trapezoid_mf, [75, 88, 99.9, 100, 1.0]    # LMF (Start 75 vs Med Koniec 80 -> 5 jednostek zakładki)
    )

    # 3. Głośność (Volume) - Wyjście też warto lekko poszerzyć
    vol_low = IT2FS(vol_dom, 
        trapezoid_mf, [0.0, 0.001, 20, 50, 1.0], 
        trapezoid_mf, [0.0, 0.001, 25, 45, 1.0]
    )
    vol_med = IT2FS(vol_dom, 
        trapezoid_mf, [30, 45, 55, 75, 1.0], 
        trapezoid_mf, [35, 48, 52, 65, 1.0]
    )
    vol_high = IT2FS(vol_dom, 
        trapezoid_mf, [55, 75, 99.9, 100, 1.0], 
        trapezoid_mf, [60, 80, 99.9, 100, 1.0]
    )

    # Konfiguracja systemu
    system.add_input_variable("Speed")
    system.add_input_variable("Noise")
    system.add_output_variable("Volume")

    # BAZA REGUŁ
    system.add_rule([("Speed", speed_low), ("Noise", noise_quiet)], [("Volume", vol_low)])
    system.add_rule([("Speed", speed_low), ("Noise", noise_med)], [("Volume", vol_low)])
    system.add_rule([("Speed", speed_low), ("Noise", noise_loud)], [("Volume", vol_med)])
    system.add_rule([("Speed", speed_med), ("Noise", noise_quiet)], [("Volume", vol_low)])
    system.add_rule([("Speed", speed_med), ("Noise", noise_med)], [("Volume", vol_med)])
    system.add_rule([("Speed", speed_med), ("Noise", noise_loud)], [("Volume", vol_high)])
    system.add_rule([("Speed", speed_high), ("Noise", noise_quiet)], [("Volume", vol_med)])
    system.add_rule([("Speed", speed_high), ("Noise", noise_med)], [("Volume", vol_high)])
    system.add_rule([("Speed", speed_high), ("Noise", noise_loud)], [("Volume", vol_high)])

    return system, vol_dom

# --- 2. CZĘŚĆ ON (SYMULACJA TRASY) ---
def run_simulation():
    # Ustalanie ścieżki do docs/imgs (działa z poziomu root i control)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir) # Wychodzimy z 'control'
    output_dir = os.path.join(project_root, 'docs', 'imgs')

    # Tworzenie folderu jeśli nie istnieje
    os.makedirs(output_dir, exist_ok=True)
    print(f"Folder docelowy dla grafik: {output_dir}")

    system, vol_dom = create_navigation_controller()
    
    # Scenariusz: 60 sekund jazdy
    time_steps = np.arange(0, 60, 1)
    
    # Prędkość
    speed_sim = np.concatenate([
        np.linspace(0, 25, 15),    # Rozpędzanie
        np.full(20, 25),           # Jazda stała
        np.linspace(25, 45, 10),   # Szybkie wyprzedzanie
        np.linspace(45, 0, 15)     # Hamowanie
    ])
    
    # Hałas
    noise_sim = np.concatenate([
        np.full(10, 45),           # Cicho
        np.linspace(45, 90, 5),    # Nagły hałas
        np.full(10, 90),           # Ciężarówka
        np.linspace(90, 60, 5),    # Odjazd
        np.linspace(60, 85, 15),   # Wiatr
        np.linspace(85, 50, 15)    # Ciszej
    ])

    results = []
    print("Trwa symulacja trasy...")
    
    for t in range(len(time_steps)):
        s = speed_sim[t]
        n = noise_sim[t]
        input_val = {"Speed": s, "Noise": n}
        _, crisp_out = system.evaluate(input_val, min_t_norm, max_s_norm, {"Volume": vol_dom})
        results.append(crisp_out["Volume"][0])

    # --- PLOT 1: SIMULATION ---
    plt.figure(figsize=(10, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(time_steps, speed_sim, label='Prędkość [km/h]', color='blue', linestyle='--')
    plt.plot(time_steps, noise_sim, label='Hałas [dB]', color='orange', linestyle='--')
    plt.title('Wejścia: Warunki jazdy')
    plt.ylabel('Wartość')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(time_steps, results, label='Głośność Nawigacji [%]', color='green', linewidth=2)
    plt.title('Wyjście: Reakcja Sterownika Type-2 (Smooth)')
    plt.xlabel('Czas [s]')
    plt.ylabel('Głośność [%]')
    plt.fill_between(time_steps, results, color='green', alpha=0.1)
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    save_path_sim = os.path.join(output_dir, 'plotSimulation.png')
    plt.savefig(save_path_sim, dpi=300)
    print(f"Zapisano: {save_path_sim}")
    plt.close()

    # --- PLOT 2: SURFACE ---
    print("Generowanie powierzchni sterowania 3D...")
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    X = np.linspace(0, 50, 25) # Zwiększona rozdzielczość dla gładszego wykresu
    Y = np.linspace(40, 100, 25)
    X_grid, Y_grid = np.meshgrid(X, Y)
    Z_grid = np.zeros_like(X_grid)

    for i in range(len(X)):
        for j in range(len(Y)):
            input_val = {"Speed": X[i], "Noise": Y[j]}
            _, crisp_out = system.evaluate(input_val, min_t_norm, max_s_norm, {"Volume": vol_dom})
            Z_grid[j, i] = crisp_out["Volume"][0]

    surf = ax.plot_surface(X_grid, Y_grid, Z_grid, cmap='viridis', edgecolor='none', alpha=0.9)
    ax.set_title('Powierzchnia Sterowania (Control Surface)')
    ax.set_xlabel('Prędkość [km/h]')
    ax.set_ylabel('Hałas [dB]')
    ax.set_zlabel('Głośność [%]')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Głośność [%]')
    
    save_path_surf = os.path.join(output_dir, 'plotSurface.png')
    plt.savefig(save_path_surf, dpi=300)
    print(f"Zapisano: {save_path_surf}")
    plt.close()

if __name__ == "__main__":
    run_simulation()