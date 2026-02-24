# 3GPP TDL Channels

Generate frequency-domain TDL (Tapped Delay Line) channel matrices using [NeoRadium](https://interdigitalinc.github.io/NeoRadium/), with config-driven dataset generation and optional plotting.

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

### Single run and plotting

Use `plot_tdl_channels.py` to generate a batch of channels with fixed parameters and plot their distribution (real/imag, power, angle/magnitude). Adjust the constants at the top of the script, then run:

```bash
python plot_tdl_channels.py
```

From Python you can call `generate_tdl_channels()` from `src.tdl` directly; it returns an array of shape `(num_channels, L, K, Nr, Nt)`.
