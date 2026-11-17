# Revision 06 verification

Written on: surface-arm · codex · 2026-11-17

Prepared from published revision 05, commit `e207d46`. Micah requested GPT-6.2 Astra and GPT-6.2 Sol and confirmed no other editor was active. Micah approved the GitHub push and GitHub Pages publication on November 17, 2026.

- Source validator passed: 27 models, 250 observations, 247 numeric values and the three existing null values.
- All eight existing unit tests passed. Build, JavaScript syntax and Git whitespace checks passed.
- All 218 previous record objects, 25 previous model entries and original compiler metadata match the base data. Revision 01–05 snapshot bytes match their Git blobs. All seven initial chart hashes pass the builder's archive checks. Revision 06 snapshot equals current data.
- Both new model labels appear in the model selector, release cards and all four current Vals comparisons. All eight new comparison values were checked in the browser.
- The Astra launch button works with the keyboard and selects Astra's five effort rows. Filtering those claims to independent evidence produces the empty state. The Sol button selects its five science rows with distinct effort settings and no asserted per-task cost. The historical setup warning remains visible for the archived legal benchmark.
- Desktop at 1280 pixels and mobile at 390 pixels have no document overflow. Release cards appear side by side on desktop and stack on mobile. The Sol button also selects the correct model and setup on mobile. Temporary viewport settings were reset.
- The archived renderer still emits the MutationObserver error documented in revision 05 as reproduced on public revision 04. Initial chart files remain unchanged; current comparison and evidence controls work.

Local screenshots are `output/playwright/revision-06-desktop.jpg` and `output/playwright/revision-06-mobile.jpg` (ignored). Rendered checks used the desktop browser tools. The generated data file matches source data; the browser download flow was interrupted and was not separately verified for this revision.

Source limits: eight Vals results and 24 selected OpenAI launch-chart points were collected, with publisher, benchmark version and effort preserved. Vals' printed November 16 page update is not asserted to be an individual run date. OpenAI's science chart labels only Cost; its dollar values remain in receipt notes while per-task cost stays null. Older records were not comprehensively reverified, and no benchmark was executed. The Atlas hub and other harness contributions were not edited. The checks above cover the local build. GitHub Actions records deployment and its checks.
