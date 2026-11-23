import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "install" / "install.py"


def metadata(skill_path: Path) -> str:
    text = skill_path.read_text(encoding="utf-8")
    return text.split("---", 2)[1]


class EliSkillsTest(unittest.TestCase):
    def test_metadata_and_output_directories_are_distinct(self):
        eli = ROOT / "skills" / "eli" / "SKILL.md"
        eli5 = ROOT / "skills" / "eli5" / "SKILL.md"

        eli_metadata = metadata(eli)
        eli5_metadata = metadata(eli5)

        self.assertIn("name: eli\n", eli_metadata)
        self.assertIn("name: eli5\n", eli5_metadata)
        self.assertIn("disable-model-invocation: true", eli_metadata)
        self.assertIn("disable-model-invocation: true", eli5_metadata)
        self.assertIn(".eli/", eli.read_text(encoding="utf-8"))
        self.assertIn(".eli5/", eli5.read_text(encoding="utf-8"))
        self.assertNotIn(".eli5/", eli.read_text(encoding="utf-8"))
        self.assertNotIn(".eli/", eli5.read_text(encoding="utf-8"))

    def test_install_keeps_eli_and_eli5_separate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            unrelated = project / ".claude" / "skills" / "unrelated" / "SKILL.md"
            unrelated.parent.mkdir(parents=True)
            unrelated.write_text("keep me\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(INSTALLER),
                    "install",
                    "local",
                    "--target",
                    str(project),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            installed_eli = project / ".claude" / "skills" / "eli" / "SKILL.md"
            installed_eli5 = project / ".claude" / "skills" / "eli5" / "SKILL.md"
            self.assertTrue(installed_eli.is_file())
            self.assertTrue(installed_eli5.is_file())
            self.assertIn("name: eli\n", metadata(installed_eli))
            self.assertIn("name: eli5\n", metadata(installed_eli5))
            self.assertEqual(unrelated.read_text(encoding="utf-8"), "keep me\n")

            # Simulate alternating contexts by reading each installed skill in sequence.
            for skill_path, expected_name in (
                (installed_eli, "eli"),
                (installed_eli5, "eli5"),
                (installed_eli, "eli"),
                (installed_eli5, "eli5"),
            ):
                self.assertIn(f"name: {expected_name}\n", metadata(skill_path))


if __name__ == "__main__":
    unittest.main()
