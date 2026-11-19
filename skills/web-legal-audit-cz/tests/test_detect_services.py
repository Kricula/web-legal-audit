import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "detect_services.py"
spec = importlib.util.spec_from_file_location("detect_services", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class DetectServicesTests(unittest.TestCase):
    def test_env_and_secret_files_are_never_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".env").write_text("OPENAI_API_KEY=sk-test_SECRET_VALUE\napi.openai.com", encoding="utf-8")
            (root / "credentials.json").write_text('{"token":"ghp_123456789012345678901234"}', encoding="utf-8")
            (root / "index.html").write_text("<script src='https://api.openai.com/v1'></script>", encoding="utf-8")
            hits = mod.scan(str(root))
            self.assertEqual(len(hits), 1)
            self.assertEqual(hits[0]["file"], "index.html")
            rendered = json.dumps(hits)
            self.assertNotIn("SECRET_VALUE", rendered)
            self.assertNotIn("ghp_123", rendered)

    def test_secret_values_are_redacted_in_snippets(self):
        sample = "const api_key = sk-abcdefghijklmnopqrstuvwxyz123456;"
        result = mod.sanitize(sample)
        self.assertNotIn("abcdefghijklmnopqrstuvwxyz", result)
        self.assertIn("REDACTED", result)

    def test_quoted_secrets_with_spaces_are_redacted(self):
        sample = 'password = "do not leak this phrase"; token=abc123'
        result = mod.sanitize(sample)
        self.assertNotIn("do not leak", result)
        self.assertNotIn("abc123", result)
        self.assertIn("REDACTED", result)

    def test_secret_directories_are_excluded(self):
        self.assertIn("secrets", mod.SKIP_DIRS)
        self.assertIn("credentials", mod.SKIP_DIRS)
        self.assertIn(".ssh", mod.SKIP_DIRS)

    def test_sensitive_file_patterns(self):
        for name in [".env", ".env.production", "id_rsa", "private.key", "service-account.json", "my-secrets.txt"]:
            self.assertTrue(mod.is_sensitive_file(name), name)

    def test_markdown_disclaims_static_evidence(self):
        md = mod.to_markdown([], "site")
        self.assertIn("Statický výskyt není důkazem", md)


if __name__ == "__main__":
    unittest.main()
