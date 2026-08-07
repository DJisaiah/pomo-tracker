# Contributing to Pomo-Tracker

First off, thank you for even considering contributing to Pomo-Tracker! 

To keep the codebase clean, stable, and maintainable, all contributors are expected to follow the architecture and workflow guidelines outlined below. PRs that ignore these architectural rules will not be merged.

## 1. Local Development Setup

Pomo-Tracker is built using Python and the Flet framework. 

### Prerequisites
* Python 3.10+
* (Linux/WSL Users): You must have the necessary GStreamer plugins installed for the audio pipeline to function correctly (`gst-plugins-good`, `gst-plugins-bad`, `gst-plugins-ugly`, `gst-libav`).

### Getting Started
1. Fork the repository and clone your fork locally.
2. Add the upstream remote: `git remote add upstream https://github.com/djisaiah/pomo-tracker.git`
3. Create a virtual environment: `python3 -m venv .venv`
4. **Activate the environment** and install dependencies: 
    * activation:
        * Linux/macOS: `source .venv/bin/activate`
        * Windows (CMD): `.venv\Scripts\activate.bat`
        * Windows (PowerShell): `.venv\Scripts\Activate.ps1`
    * dependencies:
        * `pip install -e ".[dev]"` (for project and dev dependencies)
        * `pre-commit install` (install precommit hooks to avoid ruff/pyright issues)
5. Run the app: `flet run`

## 2. Architecture

### General guide
Pomo-Tracker as an app generally tries to keep its controls pretty limited in what they have access to so that things don't end up too tangled.
So be mindful of that as you contribute. There are utility classes that assist with this.

Example: **Do NOT pass `page.update()` down through component constructors.** Instead, when necessary, UI components accept the **shared** `PomoUtils` instance. `PomoUtils` acts as the single source of truth for the application state (including the SQLite database manager, Discord RPC, and audio pipeline).

You will likely also need to reference the [Flet Docs](https://flet.dev/docs/reference/):
- [Quick App Guide](https://flet.dev/docs/tutorials/calculator)
- [Controls Reference](https://flet.dev/docs/controls)

### Project layout
The project layout is relatively self explanatory. The code tries to be as self-documenting as possible. Nevertheless this is a quick guide to it:

```
src/
├── assets/           # Flet storage directory (audio, icons, etc.)
├── components/       # UI Controls for Pomo-Tracker
│   ├── base/         # Reusable foundational control parts
│   └── composite/    # Full composite controls built from base components
├── core/             # Central utility classes (PomoUtils, DB, RPC)
├── pages/            # Respective app pages in control form
└── main.py           # App entry point and initialization
```

### 📌 How to claim/pick up an issue 📌
 **If you want to work on an open issue, please leave a comment on it first. We will manually assign it to you. Please do not start working on it until it is officially assigned to you to avoid duplicate effort.**

## 3. Branching and Commits

We strictly use the **Feature Branch Workflow**. Do not submit PRs from your fork's `main` or `stable` branch.

1. Always sync your local `main` with the `upstream/main` before starting work.
   ```
   git checkout main
   git fetch upstream
   git merge upstream/main
   ```
   - you can go back to your branch after
2. Cut a new branch using a standard prefix:
   * `feature/name-of-feature`
   * `bugfix/description-of-bug`
   * `refactor/what-is-being-cleaned`
3. Keep your commits atomic. If you are fixing an open issue, include the closing keyword (e.g., `Fixes #12`) in your PR description.

## 4. Pull Request Process

1. Ensure your code meets the necessary standards.
   * commit pre-hooks & CI
      * this project uses `ruff` and `pyright` 
      * running `pre-commit run --all-files` before committing will save time
   * good quality, reasonably performant
   * consistent with repo and OOP principles
2. **Open a Pull Request against our `main` branch.**
3. Fill out the PR template completely.
4. The maintainer will review the code. If changes are requested, push the fixes to your feature branch.
5. All accepted PRs will be **Squash and Merged** into `main`. Once `main` reaches a stable state it will be merged with `stable` as part of a stable release
