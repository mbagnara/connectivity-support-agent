# Project engineering instructions

These instructions supplement higher-priority instructions; they do not override them.

- Write project artifacts and implementation responses in English.
- Preserve existing user files and repository history.
- Use Python 3.12 and a local `.venv`; keep the `src/` package layout.
- Keep core logic independently testable, separate from Streamlit and model SDKs.
- Use one `codex/` branch and PR per feature. Never develop features directly on main.
  The initial foundation bootstrap is the only authorized direct-main baseline.
- Do not merge feature PRs or deploy without explicit authorization.
- Run local validation before push. Stage explicit, scoped paths and review the
  diff and staged content. Update relevant documentation and the engineering log.
- Add meaningful tests with behavior, starting with the service-status feature;
  add pytest to CI then. Do not create trivial tests or run an empty suite.
- Do not commit credentials, virtual environments, caches, or build output.
- Do not choose a license without the owner's decision.

Verified foundation commands (activate `.venv` first):

```sh
python -m pip install -r requirements-dev.txt
python -m pip install --no-build-isolation -e '.[dev]'
python -m pip install -e '.[dev]'
python -m ruff check .
python -m ruff format --check .
python -c "import connectivity_support_agent"
```

The plain editable install is a compatibility check; use the requirements file
first for the pinned development environment. Revalidate after dependency changes.
