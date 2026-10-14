# Codex frontier model observatory

A standalone, local-first Codex contribution to Micah's Frontier Benchmark Atlas. Public model results retain their publisher, setup, source URL, source/read date, evidence type, and any derivation. No benchmark execution or overall model rank is implied.

## Review locally

Open `dist/index.html` directly in a browser. The interactive page embeds its chart renderer, JavaScript, styles and data. Supporting notes and saved data revisions live beside it. Core views are checked offline; the renderer also references pinned CDN helpers for icons and floating controls.

For a loopback preview:

```powershell
python tools/build.py
python tools/serve.py --output dist --port 8767
```

Open `http://127.0.0.1:8767/` and stop the server with Ctrl+C.

## Files

- `data.json`: current source records, model registry, compiler metadata and revision log.
- `snapshots/`: numbered historical records.
- `charts/`: the original interactive chart and source-receipt exports.
- `archive/`: original extracted data and chart hashes.
- `web/`: source template, styles and interaction code.
- `tools/`: standard-library build, source-data validation and safe loopback preview.
- `NOTES.md`: sourcing method, direct versus second-hand limits, and disclosure of the handoff chronology.
- `atlas-submission.json`: proposed registration metadata; public URLs remain empty until publication is approved.
- `dist/`: generated page and public supporting files.

## Validation

```powershell
python tools/validate_data.py
python -m unittest discover -s tests -v
python tools/build.py
```

The builder validates the records and checks the initial chart hashes before writing generated output. Each later revision should name the triggering release, correction or source change. Keep missing scores null. Record compiler identity only when known. Do not copy another agent's work into the Codex compilation.

## GitHub and the atlas

The proposed repository is `minerclass/frontier-codex-observatory`. Repository creation, pushing, Pages and the atlas manifest change require Micah's approval. Keep the working checkout in the computer's Developer folder outside OneDrive. The atlas brief remains the registration authority; its owner adds/approves the entry before it is merged or pushed.

The chart renderer references these pinned helpers: Floating UI core 1.7.3, Floating UI DOM 1.7.4, and Lucide 1.17.0, from unpkg.com. Full auxiliary controls may require a connection. Source links, the atlas link and future hosted data also require a connection. The public packet contains only model and benchmark evidence.
