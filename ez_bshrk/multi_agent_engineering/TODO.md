# TODO (pick up later)

## Output shape / runnable skeleton

- [ ] Ensure `generated_app/` output matches the intended Python layout:
  - [ ] `pyproject.toml`
  - [ ] `src/app/__init__.py`
  - [ ] `src/app/__main__.py` (supports `python -m app --help` and `--demo`)
  - [ ] `tests/test_smoke.py` (unittest; `python -m unittest`)
- [ ] Add a minimal “smoke demo” path (`--demo`) that exercises domain + services + UI.

## Pipeline robustness

- [ ] Log dynamic-task failures into `callbacks.log.jsonl` with `status=failed` and `blocking_issues`.
- [ ] Make manifest application stricter/saner if needed:
  - [ ] Decide whether to reject dotfiles / absolute paths / oversized files.
  - [ ] Decide whether `content_mode="fenced_code"` should warn vs. error when fences are missing.

## Prompt hygiene

- [ ] Keep `BuildPlan.owner_agent` constrained to the 4 agent IDs (avoid role strings / invented roles).
- [ ] Keep dynamic tasks “Python-only” (no JS/TS) and docs minimal.

## Nice-to-haves

- [ ] Add a short CLI flag for spec selection (`SPEC_FILE` is already supported).
- [ ] Add a summary file per run (e.g. `run_summary.json`) listing written files and task statuses.

