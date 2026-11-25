import contextlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = ROOT / "install" / "install.py"
sys.path.insert(0, str(INSTALLER_PATH.parent))
SPEC = importlib.util.spec_from_file_location("ys_powers_installer", INSTALLER_PATH)
assert SPEC and SPEC.loader
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)


class SkillSourcesTest(unittest.TestCase):
    def test_collision_fails_before_target_is_created(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "source"
            target_dir = Path(temp_dir) / "target" / ".claude"
            first = project_root / "skills" / "first" / "duplicate"
            second = project_root / "skills" / "second" / "duplicate"
            first.mkdir(parents=True)
            second.mkdir(parents=True)

            directories = {
                "skills/first": ("skills", "skill-bucket"),
                "skills/second": ("skills", "skill-bucket"),
            }
            stderr = io.StringIO()
            with mock.patch.object(INSTALLER, "DIRECTORIES", directories):
                with contextlib.redirect_stderr(stderr):
                    installed = INSTALLER.do_install(project_root, target_dir, "local")

            self.assertFalse(installed)
            self.assertFalse(target_dir.exists())
            self.assertIn("duplicate", stderr.getvalue())
            self.assertIn(str(first), stderr.getvalue())
            self.assertIn(str(second), stderr.getvalue())

    def test_install_is_flat_and_removes_old_source_buckets(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            old_engineering = project / ".claude" / "skills" / "engineering"
            old_productivity = project / ".claude" / "skills" / "productivity"
            old_engineering.mkdir(parents=True)
            old_productivity.mkdir(parents=True)

            result = subprocess.run(
                [
                    sys.executable,
                    str(INSTALLER_PATH),
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
            skills = project / ".claude" / "skills"
            self.assertTrue((skills / "ask-matt" / "SKILL.md").is_file())
            self.assertTrue((skills / "why" / "SKILL.md").is_file())
            self.assertTrue((skills / "eli" / "SKILL.md").is_file())
            self.assertFalse((skills / "matt").exists())
            self.assertFalse((skills / "pstack").exists())
            self.assertFalse((skills / "local").exists())
            self.assertFalse(old_engineering.exists())
            self.assertFalse(old_productivity.exists())


if __name__ == "__main__":
    unittest.main()
