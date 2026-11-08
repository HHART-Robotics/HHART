from __future__ import annotations

import json
import pathlib

from robot1.core.contract import CONTRACT

SOFTWARE = pathlib.Path(__file__).resolve().parents[2]
SPEC = SOFTWARE / "CONTRACT.md"
GOLDEN = SOFTWARE / "apps" / "web" / "src" / "core" / "contract.golden.json"
STALE = "the contract changed: run hhart contract, then pnpm test in web"


def test_the_spec_is_current():
    assert SPEC.read_text(encoding="utf-8") == CONTRACT.markdown(), STALE


def test_the_golden_fixture_is_current():
    assert json.loads(GOLDEN.read_text(encoding="utf-8")) == CONTRACT.examples(), STALE
