from __future__ import annotations

import pathlib
import re

FIRMWARE = pathlib.Path(__file__).resolve().parents[2] / "firmware" / "robot1"
CORE = FIRMWARE / "lib" / "robot1_core"
STANDARD = {"stdint.h", "stddef.h", "stdbool.h", "cstdint", "cstddef"}


def test_the_firmware_core_includes_no_hardware_headers():
    files = [f for f in CORE.iterdir() if f.suffix in {".h", ".hpp", ".c", ".cpp"}]
    assert files, f"no sources in {CORE}"
    includes = {name for f in files
                for name in re.findall(r'#include\s*[<"]([^>"]+)[>"]', f.read_text(encoding="utf-8"))}
    assert includes - STANDARD - {f.name for f in files} == set()


def test_the_firmware_feeds_a_hardware_watchdog_and_gates_the_motors_on_it():
    main = (FIRMWARE / "src" / "main.cpp").read_text(encoding="utf-8")
    assert "hw_watchdog_feed()" in main and "motorsAllowed = hw_watchdog_begin(" in main
