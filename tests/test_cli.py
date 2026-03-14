import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from shortsmaker.cli import main


class CliSmokeTest(unittest.TestCase):
    def test_default_command_reports_ready_state(self) -> None:
        buffer = io.StringIO()

        with redirect_stdout(buffer):
            exit_code = main([])

        output = buffer.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("ShortsMaker workspace is ready.", output)
        self.assertIn(str(ROOT), output)
