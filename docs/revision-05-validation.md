# Revision 05 verification

Written on: surface-arm · codex · 2026-11-12

Prepared from GitHub main `0e198dd`; the diverged Developer checkout was preserved. Publication is pending Micah's approval.

- Source validator passed: 25 models, 218 observations, 215 numeric values and three existing null values.
- All eight existing unit tests passed with bundled Python 3.12.14. Build, JavaScript syntax and Git whitespace checks passed.
- All 203 previous record objects and original compiler metadata match the prior GitHub data exactly. Revision 01–04 snapshot bytes match their Git blobs; all seven original chart hashes pass the builder's archive checks. Revision 05 snapshot equals current data.
- Browser checks at 1280 and 390 pixels found no document overflow. The two update cards display side by side on desktop and stack on mobile.
- All four current benchmark selectors display the collected Hydrogen value. The Google-table button opens the distinct cheating-adjusted Terminal-Bench 4.1 setup with own-lab and rival-table labels. Model/evidence filtering, the empty state, historical warning and keyboard benchmark selection worked.
- Browser-downloaded revision 05 JSON equals source data exactly.
- The archived renderer emits a MutationObserver error in this browser. The same error was reproduced on the existing public revision 04 page; chart files remain unchanged. The current comparisons and evidence filters worked.

Local review screenshots are in `output/playwright/` (ignored). The npm CLI could not reach the registry, so rendered checks used the desktop browser tools. The initial Windows clone converted archived files to CRLF, triggering the hash guard; restoring their exact Git blob bytes resolved the check without changing the archived sources or hashes.

Source limits: Google's detailed Hydrogen methodology PDF was linked but not readable in this review. Only model-card table settings are recorded. Older company claims were not comprehensively reverified, and no benchmark was executed. GitHub deployment has not been performed for this revision.
