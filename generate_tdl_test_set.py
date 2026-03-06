#!/usr/bin/env python3
"""
Generate TDL test set organised into 9 subfolders — one per
(delay-spread group × Doppler group) combination.

Each subfolder contains one .npy file for every (delay_spread, doppler_shift)
pair drawn from its group, plus a metadata.yaml.
"""
import argparse
from itertools import product
from pathlib import Path

import numpy as np

from src.tdl import generate_tdl_channels
from src.utils import load_config, save_config

DELAY_GROUPS = [
    ("low_delay",      "low_delay_spread"),
    ("moderate_delay", "moderate_delay_spread"),
    ("high_delay",     "high_delay_spread"),
]
DOPPLER_GROUPS = [
    ("low_mobility",      "low_doppler"),
    ("moderate_mobility", "moderate_doppler"),
    ("high_mobility",     "high_doppler"),
]


def _base_kwargs(config: dict) -> dict:
    return {
        "num_channels": config["num_channels_per_config"],
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


def run(config_path: Path, output_dir: Path) -> None:
    config = load_config(config_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    base = _base_kwargs(config)

    for (delay_tag, delay_key), (doppler_tag, doppler_key) in product(
        DELAY_GROUPS, DOPPLER_GROUPS
    ):
        delay_spreads = config[delay_key]
        doppler_shifts = config[doppler_key]
        folder_name = f"{delay_tag}_{doppler_tag}"
        folder = output_dir / folder_name
        folder.mkdir(parents=True, exist_ok=True)

        generated = []
        for delay_spread, doppler_shift in product(delay_spreads, doppler_shifts):
            name = f"delay_{delay_spread}_doppler_{doppler_shift}.npy"
            channels = generate_tdl_channels(
                **base,
                delay_spread=delay_spread,
                doppler_shift=doppler_shift,
            )
            np.save(folder / name, channels)
            generated.append({
                "file": name,
                "delay_spread_ns": delay_spread,
                "doppler_shift_hz": doppler_shift,
            })

        save_config(folder / "metadata.yaml", {
            "config_path": str(Path(config_path).resolve()),
            "folder": folder_name,
            "delay_spreads": delay_spreads,
            "doppler_shifts": doppler_shifts,
            "config": config,
            "generated": generated,
        })


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate TDL test set (9 delay×Doppler groups)."
    )
    parser.add_argument(
        "config",
        type=Path,
        nargs="?",
        default=Path("configs/tdl_test_set.yaml"),
        help="Path to YAML config (default: configs/tdl_test_set.yaml)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output/tdl_test_set"),
        help="Output directory (default: output/tdl_test_set)",
    )
    args = parser.parse_args()
    run(args.config, args.output)


if __name__ == "__main__":
    main()
