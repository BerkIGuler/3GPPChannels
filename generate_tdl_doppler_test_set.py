#!/usr/bin/env python3
"""
Generate TDL test set for two evaluation cases:

1) NMSE vs. Doppler shift (fixed delay spread): delay_spread_fixed + doppler_sweep
2) NMSE vs. Delay spread (fixed Doppler): doppler_fixed + delay_spread_sweep

Accepts a YAML config similar to tdl_a_train_val.yaml with the sweep/fixed lists.
Saves .npy files in subfolders (doppler_sweep, delay_spread_sweep) and metadata per folder.
"""
import argparse
from pathlib import Path

import numpy as np

from src.tdl import generate_tdl_channels
from src.utils import load_config, save_config


def _base_kwargs(config: dict, num_channels: int) -> dict:
    return {
        "num_channels": num_channels,
        "random_seed": config.get("random_seed", 123),
        "start_rb": config.get("start_rb", 0),
        "num_rbs": config.get("num_rbs", 10),
        "spacing": config.get("spacing", 15),
        "tx_antenna_count": config.get("tx_antenna_count", 1),
        "rx_antenna_count": config.get("rx_antenna_count", 1),
        "carrier_freq": config.get("carrier_freq", 3.5e9),
        "profile": config.get("delay_profile", "A"),
        "show_progress": config.get("show_progress", True),
    }


def run_doppler_sweep(
    config: dict,
    output_dir: Path,
    config_path: Path,
) -> None:
    """Fixed delay spread, sweep Doppler (NMSE vs. Doppler)."""
    delay_spread_fixed = config["delay_spread_fixed"]
    doppler_sweep = config["doppler_sweep"]
    num_channels = config["num_channels_per_config"]
    base = _base_kwargs(config, num_channels)
    out = output_dir / "doppler_sweep"
    out.mkdir(parents=True, exist_ok=True)
    generated = []
    for delay_spread in delay_spread_fixed:
        for doppler_shift in doppler_sweep:
            name = f"delay_spread_{delay_spread}_doppler_{doppler_shift}.npy"
            channels = generate_tdl_channels(
                **base,
                delay_spread=delay_spread,
                doppler_shift=doppler_shift,
            )
            np.save(out / name, channels)
            generated.append({
                "file": name,
                "delay_spread_ns": delay_spread,
                "doppler_shift_hz": doppler_shift,
            })
    metadata = {
        "config_path": str(config_path.resolve()),
        "mode": "nmse_vs_doppler",
        "delay_spread_fixed": delay_spread_fixed,
        "doppler_sweep": doppler_sweep,
        "config": config,
        "generated": generated,
    }
    save_config(out / "metadata.yaml", metadata)


def run_delay_spread_sweep(
    config: dict,
    output_dir: Path,
    config_path: Path,
) -> None:
    """Fixed Doppler, sweep delay spread (NMSE vs. Delay spread)."""
    doppler_fixed = config["doppler_fixed"]
    delay_spread_sweep = config["delay_spread_sweep"]
    num_channels = config["num_channels_per_config"]
    base = _base_kwargs(config, num_channels)
    out = output_dir / "delay_spread_sweep"
    out.mkdir(parents=True, exist_ok=True)
    generated = []
    for doppler_shift in doppler_fixed:
        for delay_spread in delay_spread_sweep:
            name = f"doppler_{doppler_shift}_delay_spread_{delay_spread}.npy"
            channels = generate_tdl_channels(
                **base,
                delay_spread=delay_spread,
                doppler_shift=doppler_shift,
            )
            np.save(out / name, channels)
            generated.append({
                "file": name,
                "doppler_shift_hz": doppler_shift,
                "delay_spread_ns": delay_spread,
            })
    metadata = {
        "config_path": str(config_path.resolve()),
        "mode": "nmse_vs_delay_spread",
        "doppler_fixed": doppler_fixed,
        "delay_spread_sweep": delay_spread_sweep,
        "config": config,
        "generated": generated,
    }
    save_config(out / "metadata.yaml", metadata)


def run(config_path: Path, output_dir: Path) -> None:
    config = load_config(config_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    has_doppler_sweep = "delay_spread_fixed" in config and "doppler_sweep" in config
    has_delay_spread_sweep = "doppler_fixed" in config and "delay_spread_sweep" in config
    if not has_doppler_sweep and not has_delay_spread_sweep:
        raise ValueError(
            "Config must define either (delay_spread_fixed + doppler_sweep) "
            "or (doppler_fixed + delay_spread_sweep) (or both)."
        )
    if has_doppler_sweep:
        run_doppler_sweep(config, output_dir, config_path)
    if has_delay_spread_sweep:
        run_delay_spread_sweep(config, output_dir, config_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate TDL test set for NMSE vs. Doppler and NMSE vs. Delay spread."
    )
    parser.add_argument(
        "config",
        type=Path,
        nargs="?",
        default=Path("configs/tdl_doppler_test_set.yaml"),
        help="Path to YAML config (default: configs/tdl_doppler_test_set.yaml)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output/tdl_doppler_test_set"),
        help="Output directory (default: output/tdl_doppler_test_set)",
    )
    args = parser.parse_args()
    run(args.config, args.output)


if __name__ == "__main__":
    main()
