# Execution Tranche: migration and rollback

Scope: REQ-004 plus its REQ-005 verification in SPEC.md. STATE.md records the accepted
REQ-001..003 storage/CLI prerequisite. No whole-program plan exists; this document
does not replace one or claim that the full specification is implemented.

1. In notes.py, validate the entire legacy notes.json array before the first write.
   Preserve existing JSONL data and the blank-input guard. Malformed input changes
   neither source nor target. Resolve any unexpected dual-store state before writing.
2. Before switching to JSONL, preserve the exact legacy bytes in notes.json.bak and
   refuse to overwrite a different existing rollback copy. Carry every note over in
   order, then append the new note. Keep the migration idempotent on subsequent writes.
3. In test_notes.py, cover ordered preservation, exact rollback bytes, malformed data,
   blank input, repeated writes and backup conflicts in temporary directories.

This request stops at the plan. Migration implementation and full-spec verification
remain undelivered. No unrelated planning or reapproval is needed for these settled
prerequisites.
