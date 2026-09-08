import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CLI = Path(__file__).with_name('notes.py').resolve()


class NotesTests(unittest.TestCase):
    def test_complete_flow(self):
        with tempfile.TemporaryDirectory() as raw:
            work = Path(raw)
            def run(*args):
                return subprocess.run([sys.executable, '-I', '-S', '-B', str(CLI), *args], cwd=work, capture_output=True, text=True)
            legacy = b'["first", "second"]\n'
            (work / 'notes.json').write_bytes(legacy)
            self.assertEqual(run('add', 'third').returncode, 0)
            self.assertEqual(run('list').stdout, 'first\nsecond\nthird\n')
            self.assertEqual((work / 'notes.json.bak').read_bytes(), legacy)
            before = (work / 'notes.jsonl').read_bytes()
            self.assertNotEqual(run('add', '  ').returncode, 0)
            self.assertEqual((work / 'notes.jsonl').read_bytes(), before)
            self.assertEqual(run('add', 'fourth').returncode, 0)
            self.assertEqual(run('list').stdout, 'first\nsecond\nthird\nfourth\n')

    def test_invalid_legacy_is_unchanged(self):
        for legacy in ('{', '["ok", null]', '{}'):
            with self.subTest(legacy=legacy), tempfile.TemporaryDirectory() as raw:
                work = Path(raw)
                (work / 'notes.json').write_text(legacy)
                result = subprocess.run([sys.executable, '-I', '-S', '-B', str(CLI), 'add', 'x'], cwd=work, capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual({p.name for p in work.iterdir()}, {'notes.json'})
                self.assertEqual((work / 'notes.json').read_text(), legacy)
