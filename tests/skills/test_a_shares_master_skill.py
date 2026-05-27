from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from src.cli import normalize_filters
from src.config import Config
from src.skill import ASharesSkill


REPO_ROOT = Path(__file__).resolve().parents[2]


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    assert lines[0] == "---"
    payload: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            break
        key, value = line.split(":", 1)
        payload[key.strip()] = value.strip()
    return payload


def extract_sections(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.startswith("## ")]


class SkillCompatibilityTests(unittest.TestCase):
    def test_config_defaults_to_offline_mode(self) -> None:
        config = Config.from_env()
        self.assertTrue(config.offline_mode)
        self.assertTrue(config.validate())

    def test_self_check_is_available_without_credentials(self) -> None:
        payload = ASharesSkill().self_check()
        self.assertTrue(payload["config_valid"])
        self.assertIn("diagnose", payload["supported_scenarios"])

    def test_diagnose_returns_actionable_result(self) -> None:
        payload = ASharesSkill().diagnose("300750", date="2026-05-28")
        self.assertEqual(payload["risk"]["risk_level"], "R1")
        self.assertIn(payload["conclusion"]["action"], {"可以买", "观望", "不买"})
        self.assertGreater(payload["conclusion"]["target_price"], payload["conclusion"]["stop_loss"])

    def test_risk_scan_blocks_stocks_with_red_flags(self) -> None:
        payload = ASharesSkill().risk("600290", "2026-04-25")
        self.assertEqual(payload["risk_level"], "R3")
        self.assertIn("退市预警", payload["red_flags"])

    def test_stock_picker_accepts_comma_separated_filters(self) -> None:
        self.assertEqual(normalize_filters(["basic,tech"]), ["basic", "tech"])

    def test_run_skill_cli_outputs_json(self) -> None:
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run(
            [sys.executable, "scripts/run_skill.py", "--format", "json", "risk", "--code", "300750"],
            cwd=REPO_ROOT,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["stock_code"], "300750")

    def test_skill_frontmatter_is_agent_friendly(self) -> None:
        text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        metadata = json.loads(frontmatter["metadata"])
        self.assertEqual(frontmatter["name"], "a-shares-master")
        self.assertEqual(frontmatter["user-invocable"], "true")
        description = frontmatter["description"].strip('"')
        self.assertLessEqual(len(description), 60)
        self.assertTrue(description.endswith("."))
        self.assertEqual(frontmatter["platforms"], "[linux, macos]")
        self.assertEqual(metadata["openclaw"]["skillKey"], "a-shares-master")
        self.assertIn("python3", metadata["openclaw"]["requires"]["bins"])
        env_vars = {item["name"] for item in metadata["openclaw"]["envVars"]}
        self.assertIn("A_SHARE_SKILL_OFFLINE_MODE", env_vars)
        self.assertEqual(metadata["hermes"]["category"], "research")
        self.assertIn("stocks", metadata["hermes"]["tags"])
        self.assertIn("## Verification", text)

    def test_skill_body_follows_hermes_section_order(self) -> None:
        text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("# A-Shares Master Skill", text)
        sections = extract_sections(text)
        self.assertEqual(
            sections,
            [
                "## When To Use",
                "## Prerequisites",
                "## How To Run",
                "## Quick Reference",
                "## Procedure",
                "## Pitfalls",
                "## Verification",
            ],
        )

    def test_run_tests_script_supports_single_test_target(self) -> None:
        if os.environ.get("A_SHARE_SKILL_NESTED_TEST") == "1":
            return
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        env["A_SHARE_SKILL_NESTED_TEST"] = "1"
        result = subprocess.run(
            [
                "sh",
                "scripts/run_tests.sh",
                "tests/skills/test_a_shares_master_skill.py",
            ],
            cwd=REPO_ROOT,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        output = result.stdout + result.stderr
        self.assertIn("OK", output)


if __name__ == "__main__":
    unittest.main()
