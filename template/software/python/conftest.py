"""robot1 on sys.path without install, plus hhart inside HHART repo"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
# Outside HHART repo, hhart comes from pip
for src in (HERE / "src", HERE.parents[2] / "python" / "src"):
    if src.is_dir() and str(src) not in sys.path:
        sys.path.append(str(src))
