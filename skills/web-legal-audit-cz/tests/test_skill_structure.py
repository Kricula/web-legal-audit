import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SkillStructureTests(unittest.TestCase):
    def test_skill_frontmatter_required_fields(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        front = text.split("---", 2)[1]
        self.assertRegex(front, r"(?m)^name:\s*web-legal-audit-cz\s*$")
        self.assertRegex(front, r"(?m)^description:\s*.+$")
        self.assertRegex(front, r'(?m)^  version:\s*"2\.1\.0"\s*$')

    def test_all_markdown_links_to_local_files_resolve(self):
        for file in ROOT.rglob("*.md"):
            content = file.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", content):
                if target.startswith(("http://", "https://", "#", "mailto:", "/")):
                    continue
                local = (file.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(local.exists(), f"Broken link in {file.relative_to(ROOT)}: {target}")

    def test_required_directories_and_files_exist(self):
        for rel in ["SKILL.md", "README.md", "LICENSE", "scripts/detect_services.py", "references/pravni-metodika.md", "references/zdroje-a-judikatura.md", "tests/test_detect_services.py"]:
            self.assertTrue((ROOT / rel).is_file(), rel)


if __name__ == "__main__":
    unittest.main()
