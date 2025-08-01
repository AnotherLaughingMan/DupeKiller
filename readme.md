# DupeKiller

DupeKiller is a lightweight GUI utility for identifying and removing duplicate files based on filename patterns. Designed for simplicity and speed, it helps clean up cluttered directories with minimal fuss.

## Features

- 📁 Manual folder selection via dialog
- 🧠 Duplicate detection using filename pattern matching (`* - Copy*`)
- 👀 Scrollable preview of detected duplicates
- 🗑️ File deletion with optional dry-run mode
- 🧪 Dry-run toggle to simulate deletion safely
- 🎨 Color-coded feedback:
  - 🔴 Red for deleted files
  - 🟠 Orange for dry-run previews
- 📄 Log file creation with timestamp
- 🚪 Option to auto-open log file after deletion
- 📊 Footer labels showing version and duplicate count

## Why filename-based?

DupeKiller uses filename pattern matching (e.g. `* - Copy*`) instead of hash or byte-level comparison. This decision was driven by a specific—and frustrating—real-world problem:

Microsoft OneDrive, in its infinite wisdom, often creates unnecessary file copies rather than overwriting existing ones. Instead of syncing cleanly, it litters your folders with duplicates like `file - Copy (1).txt`, `file - Copy (2).txt`, and so on. These aren't true duplicates in content—they're just redundant clutter.

DupeKiller was built to target this mess directly. By focusing on predictable filename patterns, it offers a fast, no-nonsense way to clean up what OneDrive left behind—without the overhead of hashing or deep file inspection.

It’s a pragmatic solution to a modern annoyance.

## Installation

DupeKiller is distributed as a standalone `.exe` built with PyInstaller. No Python installation or dependencies required.

1. Download the latest release from the [Releases](#) page
2. Run `DupeKiller.exe`

## Usage

1. Launch the application
2. Select a folder to scan
3. Review the list of detected duplicates
4. Toggle dry-run mode if desired
5. Click "Delete" to remove duplicates or simulate deletion
6. View the log file for details

## Known Issues

- ❗ No undo functionality after deletion  
  Once files are deleted, they’re gone. Use dry-run mode to preview before committing.

- ⚠️ False positives possible  
  Detection is based solely on filename patterns. Files with similar names but different content may be flagged.

- 🧹 No recursive folder scanning  
  Only the selected folder is scanned—subdirectories are ignored for now.

- 🧊 UI may freeze briefly during large scans  
  Performance is generally smooth, but very large directories may cause temporary lag.

## License

This project is licensed under the MIT License. See `license.txt` for details.

## Changelog

See `changelog.md` for version history and feature progression.
