import io
import json
import shutil
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from shortsmaker.cli import main
from shortsmaker.job import create_plan, prepare_renders


class CliSmokeTest(unittest.TestCase):
    def test_default_command_reports_ready_state(self) -> None:
        buffer = io.StringIO()

        with redirect_stdout(buffer):
            exit_code = main([])

        output = buffer.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("ShortsMaker workspace is ready.", output)
        self.assertIn(str(ROOT), output)
        self.assertIn("Default renderer: remotion", output)

    def test_plan_generation_creates_multilingual_manifest(self) -> None:
        profile_path = ROOT / "input" / "profiles" / "sample_saju.json"
        manifest, plan_path = create_plan(profile_path, languages=["en", "ko"])

        self.addCleanup(lambda: shutil.rmtree(plan_path.parent, ignore_errors=True))

        self.assertTrue(plan_path.exists())
        self.assertEqual(manifest["targets"]["languages"], ["en", "ko"])
        self.assertEqual(len(manifest["languages"]), 2)
        self.assertIn("selected_variant", manifest["languages"][0])

    def test_render_prep_writes_props_without_audio(self) -> None:
        profile_path = ROOT / "input" / "profiles" / "sample_saju.json"
        _, plan_path = create_plan(profile_path, languages=["en"])
        self.addCleanup(lambda: shutil.rmtree(plan_path.parent, ignore_errors=True))

        plan = prepare_renders(plan_path, selected_language="en")
        props_path = Path(plan["languages"][0]["render_artifact"]["props_path"])
        props = json.loads(props_path.read_text(encoding="utf-8"))

        self.assertTrue(props_path.exists())
        self.assertIsNone(props["narration"]["audioSrc"])
