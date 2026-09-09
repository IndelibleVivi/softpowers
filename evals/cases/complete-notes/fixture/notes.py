"""Incomplete CLI: add only, no validation or migration yet."""
import json
from pathlib import Path
import sys

if sys.argv[1] == 'add':
    with Path('notes.jsonl').open('a') as out:
        out.write(json.dumps({'text': sys.argv[2]}) + '\n')
