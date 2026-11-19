"""Testy repozitáře: shoda verzí, manifesty pluginů a instalátory.

Spuštění z kořene repozitáře:
    python3 -m unittest discover -s tests -v
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "web-legal-audit-cz"
SKILL_DIR = ROOT / "skills" / SKILL_NAME

sys.path.insert(0, str(ROOT / "tools"))
import set_version  # noqa: E402


class VersionSyncTests(unittest.TestCase):
    def test_all_versions_match(self):
        versions = set_version.current_versions()
        missing = [k for k, v in versions.items() if v is None]
        self.assertFalse(missing, f"Chybí verze v: {missing}")
        self.assertEqual(len(set(versions.values())), 1, f"Verze se neshodují: {versions}")

    def test_release_tag_matches_version(self):
        ref = os.environ.get("GITHUB_REF", "")
        if not ref.startswith("refs/tags/v"):
            self.skipTest("Neběží pro tag vydání.")
        version = set_version.current_versions()["SKILL.md metadata.version"]
        self.assertEqual(ref[len("refs/tags/v"):], version, "Tag neodpovídá verzi skillu.")


class PluginManifestTests(unittest.TestCase):
    def load(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_claude_marketplace(self):
        market = self.load(".claude-plugin/marketplace.json")
        for field in ("name", "owner", "plugins"):
            self.assertIn(field, market)
        self.assertEqual(len(market["plugins"]), 1)
        entry = market["plugins"][0]
        self.assertEqual(entry["name"], SKILL_NAME)
        self.assertEqual(entry["source"], "./")
        self.assertNotIn("..", entry["source"])

    def test_claude_plugin_manifest_matches_entry(self):
        plugin = self.load(".claude-plugin/plugin.json")
        market = self.load(".claude-plugin/marketplace.json")
        self.assertEqual(plugin["name"], market["plugins"][0]["name"])
        skills = ROOT / plugin["skills"]
        self.assertTrue((skills / SKILL_NAME / "SKILL.md").is_file())

    def test_agents_marketplace(self):
        market = self.load(".agents/plugins/marketplace.json")
        entry = market["plugins"][0]
        self.assertEqual(entry["name"], SKILL_NAME)
        self.assertEqual(entry["source"], {"source": "local", "path": "./"})
        self.assertIn(entry["policy"]["installation"], {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"})
        self.assertIn("category", entry)
        self.assertIn("displayName", market["interface"])


@unittest.skipIf(shutil.which("bash") is None, "bash není k dispozici")
class InstallerTests(unittest.TestCase):
    def run_sh(self, *args, home):
        env = dict(os.environ, HOME=home)
        return subprocess.run(["bash", str(ROOT / "install.sh"), *args], cwd=home, env=env,
                              capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=120)

    def test_install_and_uninstall_project(self):
        with tempfile.TemporaryDirectory() as home:
            proj = Path(home, "proj")
            proj.mkdir()
            r = self.run_sh("--agent", "claude-code,cursor,codex", "--project", str(proj), home=home)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((proj / ".claude/skills" / SKILL_NAME / "SKILL.md").is_file())
            self.assertTrue((proj / ".agents/skills" / SKILL_NAME / "SKILL.md").is_file())
            r = self.run_sh("--agent", "claude-code,cursor", "--project", str(proj), "--uninstall", home=home)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertFalse((proj / ".claude/skills" / SKILL_NAME).exists())

    def test_global_all_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as home:
            r = self.run_sh("--agent", "all", "--global", "--dry-run", "--force", home=home)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual([p for p in Path(home).rglob("SKILL.md")], [])

    def test_zip_excludes_dev_files(self):
        with tempfile.TemporaryDirectory() as home:
            out = Path(home, "skill.zip")
            r = self.run_sh("--zip", str(out), home=home)
            self.assertEqual(r.returncode, 0, r.stderr)
            names = zipfile.ZipFile(out).namelist()
            self.assertIn(f"{SKILL_NAME}/SKILL.md", names)
            for bad in ("/tests/", "/README.md", "/CHANGELOG.md", "__pycache__"):
                self.assertFalse([n for n in names if bad in n], f"ZIP obsahuje {bad}")

    def test_invalid_ref_and_agent_fail(self):
        with tempfile.TemporaryDirectory() as home:
            self.assertNotEqual(self.run_sh("--agent", "cursor", "--ref", "x;y", home=home).returncode, 0)
            self.assertNotEqual(self.run_sh("--agent", "vim", "--global", home=home).returncode, 0)


if __name__ == "__main__":
    unittest.main()
