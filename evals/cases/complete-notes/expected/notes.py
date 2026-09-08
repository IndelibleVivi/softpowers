"""Local Notes CLI with ordered JSONL storage and first-write legacy migration."""
import json
import os
from pathlib import Path
import sys
import tempfile


def add(text):
    if not text.strip():
        raise ValueError('blank note')
    store, legacy, backup = map(Path, ('notes.jsonl', 'notes.json', 'notes.json.bak'))
    if not store.exists() and legacy.exists():
        original = legacy.read_bytes()
        notes = json.loads(original)
        if not isinstance(notes, list) or not all(isinstance(n, str) and n.strip() for n in notes):
            raise ValueError('invalid legacy notes')
        if backup.exists() and backup.read_bytes() != original:
            raise ValueError('rollback copy conflict')
        if not backup.exists():
            with backup.open('xb') as out:
                out.write(original)
        payload = ''.join(json.dumps({'text': n}, ensure_ascii=False) + '\n' for n in [*notes, text])
        name = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir='.', delete=False) as out:
                name = out.name
                out.write(payload)
                out.flush()
                os.fsync(out.fileno())
            os.replace(name, store)
        finally:
            if name and Path(name).exists():
                Path(name).unlink()
    else:
        with store.open('a', encoding='utf-8') as out:
            out.write(json.dumps({'text': text}, ensure_ascii=False) + '\n')


def main():
    if len(sys.argv) == 3 and sys.argv[1] == 'add':
        add(sys.argv[2])
    elif sys.argv[1:] == ['list']:
        store = Path('notes.jsonl')
        if store.exists():
            for line in store.read_text(encoding='utf-8').splitlines():
                print(json.loads(line)['text'])
    else:
        raise ValueError('usage: notes.py add <text> | list')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
