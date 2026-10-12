## What changed and why?

<!-- Summarize the change and who it helps. For resources, explain relevance. One line per resource entry. -->

## Checks

- [ ] `python3 scripts/check-examples.py` (if examples changed; use `--write` to regenerate the index)
- [ ] `python3 scripts/check-catalog.py` (if README or `catalog/` changed)
- [ ] `python3 -m unittest discover -s tests` (if scripts or `field_guide/` changed)
- [ ] No Chinese-origin models or their fine-tunes (see CONTRIBUTING.md)
- [ ] `python3 -m compileall -q examples scripts` (if Python changed)
- [ ] `npx --yes awesome-lint README.md` (if README changed)
- [ ] Links checked with `python3 scripts/check-links.py`, or explain why not
- [ ] Docs/index updated and no secrets or private data included

## Evidence / limitations

<!-- Link to the canonical resource or state what could not be tested (e.g., model download, API key, paid service). -->
