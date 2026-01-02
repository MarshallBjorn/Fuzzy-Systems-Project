import numpy as np
import matplotlib.pyplot as plt
from pyit2fls import (
    IT2FLS,
    IT2FS,
    trapezoid_mf,
    tri_mf,
    min_t_norm,
    max_s_norm,
    IT2FS_plot,
)

system = IT2FLS()

speed_dom = np.linspace(0, 50, 1000)
noise_dom = np.linspace(40, 100, 1000)
vol_dom = np.linspace(0, 100, 1000)

speed_low = IT2FS(
    speed_dom,
    trapezoid_mf,
    [0.0, 0.001, 10, 18, 1.0],
    trapezoid_mf,
    [0.0, 0.001, 12, 15, 1.0],
)
speed_med = IT2FS(speed_dom, tri_mf, [10, 20, 30, 1.0], tri_mf, [12, 20, 28, 1.0])
speed_high = IT2FS(
    speed_dom,
    trapezoid_mf,
    [25, 32, 49.9, 50, 1.0],
    trapezoid_mf,
    [28, 35, 49.9, 50, 1.0],
)

noise_quiet = IT2FS(
    noise_dom,
    trapezoid_mf,
    [40, 40.001, 55, 65, 1.0],
    trapezoid_mf,
    [40, 40.001, 58, 62, 1.0],
)
noise_med = IT2FS(noise_dom, tri_mf, [55, 67, 80, 1.0], tri_mf, [58, 67, 77, 1.0])
noise_loud = IT2FS(
    noise_dom,
    trapezoid_mf,
    [75, 85, 99.9, 100, 1.0],
    trapezoid_mf,
    [78, 88, 99.9, 100, 1.0],
)

vol_low = IT2FS(
    vol_dom,
    trapezoid_mf,
    [0.0, 0.001, 20, 45, 1.0],
    trapezoid_mf,
    [0.0, 0.001, 25, 40, 1.0],
)
vol_med = IT2FS(vol_dom, tri_mf, [30, 50, 70, 1.0], tri_mf, [35, 50, 65, 1.0])
vol_high = IT2FS(
    vol_dom,
    trapezoid_mf,
    [60, 75, 99.9, 100, 1.0],
    trapezoid_mf,
    [65, 80, 99.9, 100, 1.0],
)

system.add_input_variable("Speed")
system.add_input_variable("Noise")
system.add_output_variable("Volume")

system.add_rule([("Speed", speed_low), ("Noise", noise_quiet)], [("Volume", vol_low)])
system.add_rule([("Speed", speed_low), ("Noise", noise_med)], [("Volume", vol_low)])
system.add_rule([("Speed", speed_low), ("Noise", noise_loud)], [("Volume", vol_med)])
system.add_rule([("Speed", speed_med), ("Noise", noise_quiet)], [("Volume", vol_low)])
system.add_rule([("Speed", speed_med), ("Noise", noise_med)], [("Volume", vol_med)])
system.add_rule([("Speed", speed_med), ("Noise", noise_loud)], [("Volume", vol_high)])
system.add_rule([("Speed", speed_high), ("Noise", noise_quiet)], [("Volume", vol_med)])
system.add_rule([("Speed", speed_high), ("Noise", noise_med)], [("Volume", vol_high)])
system.add_rule([("Speed", speed_high), ("Noise", noise_loud)], [("Volume", vol_high)])

input_val = {"Speed": 35, "Noise": 95}

it2_out, crisp_out = system.evaluate(
    input_val, min_t_norm, max_s_norm, {"Volume": vol_dom}
)

volume_result = crisp_out["Volume"][0]
print(f"Wyjściowa głośność nawigacji: {volume_result:.2f} %")


# plt.figure()
# it2_out["Volume"].plot(title="Wynikowy obszar głośności (FOU)")
# plt.axvline(x=crisp_out["Volume"][0], color="r", linestyle="--", label="Defuzyfikacja")
# plt.legend()

# plt.show()
