from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "codex"
SKILLS_ROOT = PLUGIN_ROOT / "skills"
MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
EXPECTED_SKILLS = {
    "hardware-cdc",
    "hardware-constraints",
    "hardware-rtl-design",
    "hardware-synthesis",
    "hardware-verification",
}


def test_marketplace_source_matches_manifest() -> None:
    manifest = json.loads(
        (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    entries = [item for item in marketplace["plugins"] if item["name"] == manifest["name"]]

    assert len(entries) == 1
    source = entries[0]["source"]
    assert source["source"] == "local"
    assert (REPO_ROOT / source["path"]).resolve() == PLUGIN_ROOT.resolve()


def test_plugin_contains_only_the_five_supported_skills() -> None:
    actual = {path.parent.name for path in SKILLS_ROOT.glob("*/SKILL.md")}

    assert actual == EXPECTED_SKILLS
    assert not list(SKILLS_ROOT.glob("*/scripts"))


def test_skill_references_resolve_within_their_skill() -> None:
    for skill_md in SKILLS_ROOT.glob("*/SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        for relative in re.findall(r"`(references/[^`]+\.md)`", text):
            assert (skill_md.parent / relative).is_file(), f"{skill_md}: {relative}"


def test_rtl_skill_has_no_duplicate_style_checklist() -> None:
    rtl_skill = SKILLS_ROOT / "hardware-rtl-design"

    assert not (rtl_skill / "references" / "style-checklist.md").exists()
    assert "style-checklist.md" not in (rtl_skill / "SKILL.md").read_text(
        encoding="utf-8"
    )


def test_overlapping_skill_content_stays_lean() -> None:
    limits = {
        "hardware-rtl-design": 90,
        "hardware-verification": 55,
        "hardware-synthesis": 65,
    }
    over_limit = {}
    for skill, limit in limits.items():
        lines = (SKILLS_ROOT / skill / "SKILL.md").read_text(encoding="utf-8").splitlines()
        if len(lines) > limit:
            over_limit[skill] = (len(lines), limit)

    assert not over_limit


def test_constraints_metadata_does_not_claim_pcf_support() -> None:
    metadata = (
        SKILLS_ROOT / "hardware-constraints" / "agents" / "openai.yaml"
    ).read_text(encoding="utf-8")

    assert "PCF" not in metadata


def test_public_metadata_does_not_advertise_removed_scanners() -> None:
    paths = [
        PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
        REPO_ROOT / "README.md",
        REPO_ROOT / "README.en.md",
    ]

    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        assert "scanning script" not in text
        assert "扫描脚本" not in text
        assert "rtl_audit.py" not in text
        assert "cdc_scan.py" not in text


def test_gray_pointer_reference_allows_multiple_counts_of_staleness() -> None:
    reference = (
        SKILLS_ROOT
        / "hardware-cdc"
        / "references"
        / "cdc-rdc-reference.md"
    ).read_text(encoding="utf-8")

    assert "one count behind" not in reference
    assert "multiple source increments" in reference
    assert "bus-skew" in reference
