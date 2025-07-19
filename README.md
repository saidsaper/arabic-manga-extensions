# Komikku Extension Repository

This is a minimal Komikku extension repository with support for MangaDex (English and Arabic).

## Installation

### Option 1: GitHub Hosting

1. Upload `index.min.json` to a GitHub repository (e.g. `https://raw.githubusercontent.com/yourname/komikku-repo/main/index.min.json`)
2. In Komikku → Extensions → Add Repository → Paste the raw GitHub URL

### Option 2: Manual Installation

1. Extract this ZIP on Linux to:
   ```
   ~/.local/share/komikku/extensions/
   ```
2. Restart Komikku and the extension will appear in the list.

## Structure

- `index.min.json`: Lists all extensions.
- Each extension must define base URL, endpoints, languages, etc.

