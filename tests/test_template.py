import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate import validate, AGENTS, SKILLS

class TemplateTests(unittest.TestCase):
    def test_valid_configuration(self):
        self.assertEqual(validate(ROOT), [])

    def test_expected_team_size(self):
        self.assertEqual(len(AGENTS), 9)
        self.assertEqual(len(SKILLS), 7)

    def test_no_secret_files(self):
        self.assertFalse((ROOT / ".env").exists())
        self.assertFalse((ROOT / "id_rsa").exists())

if __name__ == "__main__":
    unittest.main()
