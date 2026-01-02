import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
    # Prędkość (Speed)
    speed_low = IT2FS(speed_dom, trapezoid_mf, [0.0, 0.001, 10, 18, 1.0], trapezoid_mf, [0.0, 0.001, 12, 15, 1.0])
    speed_med = IT2FS(speed_dom, tri_mf, [10, 20, 30, 1.0], tri_mf, [12, 20, 28, 1.0])
    speed_high = IT2FS(speed_dom, trapezoid_mf, [25, 32, 49.9, 50, 1.0], trapezoid_mf, [28, 35, 49.9, 50, 1.0])

    # Hałas (Noise)
    noise_quiet = IT2FS(noise_dom, trapezoid_mf, [40, 40.001, 55, 65, 1.0], trapezoid_mf, [40, 40.001, 58, 62, 1.0])
    noise_med = IT2FS(noise_dom, tri_mf, [55, 67, 80, 1.0], tri_mf, [58, 67, 77, 1.0])
    noise_loud = IT2FS(noise_dom, trapezoid_mf, [75, 85, 99.9, 100, 1.0], trapezoid_mf, [78, 88, 99.9, 100, 1.0])

    # ZMIENNA WYJŚCIOWA
    # Głośność (Volume)
    vol_low = IT2FS(vol_dom, trapezoid_mf, [0.0, 0.001, 20, 45, 1.0], trapezoid_mf, [0.0, 0.001, 25, 40, 1.0])
    vol_med = IT2FS(vol_dom, tri_mf, [30, 50, 70, 1.0], tri_mf, [35, 50, 65, 1.0])
    vol_high = IT2FS(vol_dom, trapezoid_mf, [60, 75, 99.9, 100, 1.0], trapezoid_mf, [65, 80, 99.9, 100, 1.0])

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
    system, vol_dom = create_navigation_controller()
    
    # Scenariusz: 60 sekund jazdy
    time_steps = np.arange(0, 60, 1)
    
    # Generujemy dane testowe (symulacja jazdy)
    # Prędkość: Start -> Rozpędzanie -> Stała -> Hamowanie -> Postój
    speed_sim = np.concatenate([
        np.linspace(0, 25, 15),    # Rozpędzanie 0-15s
        np.full(20, 25),           # Jazda stała 15-35s
        np.linspace(25, 45, 10),   # Szybkie wyprzedzanie 35-45s
        np.linspace(45, 0, 15)     # Hamowanie do zera 45-60s
    ])
    
    # Hałas: Cicho -> Nagły hałas (ciężarówka) -> Wiatr przy prędkości -> Cisza
    noise_sim = np.concatenate([
        np.full(10, 45),           # Cicha uliczka
        np.linspace(45, 90, 5),    # Nadjeżdża coś głośnego
        np.full(10, 90),           # Mija nas ciężarówka
        np.linspace(90, 60, 5),    # Ciężarówka odjeżdża
        np.linspace(60, 85, 15),   # Szum wiatru rośnie z prędkością
        np.linspace(85, 50, 15)    # Zwalniamy, ciszej
    ])

    results = []
    print("Trwa symulacja trasy... (to może chwilę potrwać)")
    
    for t in range(len(time_steps)):
        s = speed_sim[t]
        n = noise_sim[t]
        
        # Obliczenie wyjścia sterownika
        input_val = {"Speed": s, "Noise": n}
        _, crisp_out = system.evaluate(input_val, min_t_norm, max_s_norm, {"Volume": vol_dom})
        vol = crisp_out["Volume"][0]
        results.append(vol)

    # --- 3. WIZUALIZACJA DLA DOKUMENTACJI ---
    
    # Wykres 1: Przebiegi w czasie (Empiryczny dowód działania)
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
    plt.title('Wyjście: Reakcja Sterownika Type-2')
    plt.xlabel('Czas [s]')
    plt.ylabel('Głośność [%]')
    plt.fill_between(time_steps, results, color='green', alpha=0.1)
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

    # Wykres 2: Powierzchnia Sterowania (Control Surface)
    # To jest "bajer" do dokumentacji pokazujący spójność reguł
    print("Generowanie powierzchni sterowania 3D...")
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    X = np.linspace(0, 50, 20) # Prędkość (mniejsza rozdzielczość dla szybkości)
    Y = np.linspace(40, 100, 20) # Hałas
    X_grid, Y_grid = np.meshgrid(X, Y)
    Z_grid = np.zeros_like(X_grid)

    for i in range(len(X)):
        for j in range(len(Y)):
            input_val = {"Speed": X[i], "Noise": Y[j]}
            _, crisp_out = system.evaluate(input_val, min_t_norm, max_s_norm, {"Volume": vol_dom})
            Z_grid[j, i] = crisp_out["Volume"][0] # Uwaga na indeksowanie

    surf = ax.plot_surface(X_grid, Y_grid, Z_grid, cmap='viridis', edgecolor='none', alpha=0.8)
    ax.set_title('Powierzchnia Sterowania (Control Surface)')
    ax.set_xlabel('Prędkość [km/h]')
    ax.set_ylabel('Hałas [dB]')
    ax.set_zlabel('Głośność [%]')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    plt.show()

if __name__ == "__main__":
    run_simulation()