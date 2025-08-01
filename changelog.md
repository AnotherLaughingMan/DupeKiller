# changelog.md

## [v0.1] – Initial Build
- Added folder selection using `filedialog.askdirectory()`
- Implemented duplicate detection by filename pattern (`* - Copy*`)
- Basic GUI layout

## [v0.2] – Preview and Deletion
- Added scrollable text area to preview duplicates
- Implemented file deletion (unless dry-run is enabled)

## [v0.3] – Safety Features
- Introduced dry-run mode toggle to simulate deletion

## [v0.4] – Visual Feedback
- Added color-coded feedback:
  - 🔴 Red for deleted files
  - 🟠 Orange for dry-run previews

## [v0.5] – Logging
- Created log file with timestamp after deletion

## [v0.6] – Convenience
- Added toggle to auto-open log file after deletion

## [v0.7] – Footer Info
- Added version label (bottom-left)
- Added duplicate count label (bottom-right)

## [v0.9] – Layout Fixes
- Reserved footer space using `content_frame` to prevent overlap

## [v1.1] – Polish and Prioritization
- Enforced minimum window size to prevent UI squashing
- Removed branding label to prioritize functional layout
