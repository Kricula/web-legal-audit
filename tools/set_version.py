#!/usr/bin/env python3
"""Nastaví verzi skillu na jednom místě pro celý repozitář.

Použití:
    python3 tools/set_version.py 2.3.0          # přepíše verzi ve všech souborech
    python3 tools/set_version.py --check        # jen ověří, že se verze shodují

Upravuje: SKILL.md (metadata.version), .claude-plugin/plugin.json,
.claude-plugin/marketplace.json (metadata.version i verzi pluginu) a README.md
("Current version"). Záznam v CHANGELOG.md piš ručně.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "web-legal-audit-cz" / "SKILL.md"
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
MARKET = ROOT / ".claude-plugin" / "marketplace.json"
README = ROOT / "README.md"
CHANGELOG = ROOT / "skills" / "web-legal-audit-cz" / "CHANGELOG.md"

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SKILL_RE = re.compile(r'(?m)^(  version:\s*")(\d+\.\d+\.\d+)(")\s*$')
README_RE = re.compile(r"(?m)^(Current version: \*\*)(\d+\.\d+\.\d+)(\*\*)$")
CHANGELOG_RE = re.compile(r"(?m)^## (\d+\.\d+\.\d+)\b")


def current_versions():
    plugin = json.loads(PLUGIN.read_text(encoding="utf-8"))
    market = json.loads(MARKET.read_text(encoding="utf-8"))
    skill = SKILL_RE.search(SKILL.read_text(encoding="utf-8"))
    readme = README_RE.search(README.read_text(encoding="utf-8"))
    changelog = CHANGELOG_RE.search(CHANGELOG.read_text(encoding="utf-8"))
    return {
        "SKILL.md metadata.version": skill.group(2) if skill else None,
        ".claude-plugin/plugin.json version": plugin.get("version"),
        ".claude-plugin/marketplace.json metadata.version": market.get("metadata", {}).get("version"),
        ".claude-plugin/marketplace.json plugins[0].version": market["plugins"][0].get("version"),
        "README.md Current version": readme.group(2) if readme else None,
        "CHANGELOG.md poslední záznam": changelog.group(1) if changelog else None,
    }


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def set_version(version):
    if not SEMVER.match(version):
        sys.exit(f"Neplatná verze '{version}' – použij formát X.Y.Z")
    text = SKILL.read_text(encoding="utf-8")
    if not SKILL_RE.search(text):
        sys.exit("V SKILL.md chybí řádek '  version: \"X.Y.Z\"' v metadata.")
    SKILL.write_text(SKILL_RE.sub(rf"\g<1>{version}\g<3>", text, count=1), encoding="utf-8")

    plugin = json.loads(PLUGIN.read_text(encoding="utf-8"))
    plugin["version"] = version
    write_json(PLUGIN, plugin)

    market = json.loads(MARKET.read_text(encoding="utf-8"))
    market.setdefault("metadata", {})["version"] = version
    for entry in market["plugins"]:
        entry["version"] = version
    write_json(MARKET, market)

    text = README.read_text(encoding="utf-8")
    old = README_RE.search(text)
    text = README_RE.sub(rf"\g<1>{version}\g<3>", text, count=1)
    if old:  # příklady instalace konkrétní verze (…/vX.Y.Z/install.sh, --ref vX.Y.Z)
        text = re.sub(rf"\bv{re.escape(old.group(2))}\b", f"v{version}", text)
    README.write_text(text, encoding="utf-8")

    print(f"Verze nastavena na {version}.")
    if current_versions()["CHANGELOG.md poslední záznam"] != version:
        print(f"Nezapomeň přidat záznam '## {version} – datum' do {CHANGELOG.relative_to(ROOT)}.")


def check():
    versions = current_versions()
    for where, v in versions.items():
        print(f"  {v or 'CHYBÍ':10} {where}")
    if len(set(versions.values())) != 1 or None in versions.values():
        sys.exit("Verze se neshodují.")
    print(f"OK – všude {next(iter(versions.values()))}")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    check() if sys.argv[1] == "--check" else set_version(sys.argv[1])
