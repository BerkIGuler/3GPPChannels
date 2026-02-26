# 3GPP TDL Channels

Generate frequency-domain TDL (Tapped Delay Line) channel matrices using [NeoRadium](https://interdigitalinc.github.io/NeoRadium/), with config-driven dataset generation and optional plotting. By default, generated channels are normalized by their mean power (so that E[|H|²] = 1).

## Dependencies

- Python 3.12.12
- [NeoRadium 0.4.1](https://interdigitalinc.github.io/NeoRadium/html/source/installation.html)
- NumPy
- Matplotlib
- PyYAML
- tqdm

## Generating TDL Channels

### Dataset from YAML config

Generate a TDL channel dataset (one `.npy` file per delay spread and Doppler pair) from a config file:

```bash
# Default config (configs/tdl_dataset.yaml) and default output (output/tdl_dataset)
python generate_tdl_dataset.py

# Custom config and output directory
python generate_tdl_dataset.py path/to/config.yaml -o path/to/output
```

- **Config:** Edit `configs/tdl_dataset.yaml` to set `delay_spreads`, `max_doppler_shifts`, `num_channels_per_config`, and other parameters.
- **Output:** One file per pair (e.g. `delay_spread_25_doppler_100.npy`) plus `metadata.yaml` listing the config and generated files.

### Plot scripts

- **`plot_tdl_channel_specs.py`** — Generates channels for a single TDL profile (set `PROFILE` at the top), then plots real/imag, power, angle/magnitude, and power+CDF. Tune the constants and run `python plot_tdl_channel_specs.py`.
- **`plot_tdl_channel_specs_compare_profiles.py`** — Generates channels for profiles A, B, C, D, and E, prints mean power per profile, then shows the same four plot types in a 2×5 or 1×5 grid so you can compare profiles side by side. Run `python plot_tdl_channel_specs_compare_profiles.py`.

Plotting helpers live in `src.utils` (single-channel and multi-profile variants).

### Python API

From Python you can call `generate_tdl_channels()` from `src.tdl` directly; it returns an array of shape `(num_channels, L, K, Nr, Nt)`. Pass `normalize_mean_power=False` to keep the raw NeoRadium scale (mean power typically ~1–2 depending on profile).
