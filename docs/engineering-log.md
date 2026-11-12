# Engineering log

## 2026-11-12 — Foundation bootstrap

### Inspection and decisions

- The dedicated project directory was empty; no Git repository, remotes, existing
  user files, or ancestor AGENTS.md instructions were found.
- Git identity was configured for Mario Bagnara. Initial sandbox network checks
  failed DNS resolution and reported GitHub authentication unavailable. Retrying
  with network access verified authenticated GitHub login `mbagnara`; the target
  repository did not exist. No credentials were written to project files.
- Available interpreters included Python 3.14.2 and 3.12.14. Selected 3.12.14 for a
  conservative development baseline; package minimum is 3.12, with no claim of
  validation on other versions. Created `.venv` using `python3.12 -m venv .venv`.
- Official PyPI JSON metadata reported pytest 9.2.0 requires Python >=3.10,
  Ruff 0.17.5 requires >=3.7, and setuptools 84.2.1 requires >=3.10, all compatible.
  Pinned direct tools and build backend; captured resolved transitive dependencies
  and pip with `python -m pip freeze --all --exclude-editable` in requirements-dev.txt.
- Used a minimal setuptools `src/` package with no runtime dependencies. Kept
  Streamlit, provider SDKs, service-status implementation, and tests out of scope.
- Official action release pages verified checkout v6.0.2 and setup-python v6.1.0.
  CI uses those exact release tags and Python 3.12.14. Tags are version pins, not
  immutable commit pins. CI installs development pins before editable installation.
- No license selected. Book attribution follows the supplied brief; source pages
  were not available for inspection. No text or implementation was copied.

### Commands and outcomes

The following inspection commands were run: `pwd`, `ls -la`, `rg --files` for
project metadata, ancestor AGENTS.md reads, `git status --short --branch`,
`git remote -v`, `gh auth status`, `gh api user --jq .login`,
`gh repo view mbagnara/connectivity-support-agent --json nameWithOwner,isPrivate,defaultBranchRef,url`,
interpreter version/path checks, and Git identity checks. Git inspection confirmed
there was no repository; authenticated remote lookup confirmed no target repository.

Inside `.venv`, the initial editable development installation plus explicit
setuptools 84.2.1 succeeded. These validation commands also succeeded:

```sh
python -m pip install -e '.[dev]'
python -m pip install -r requirements-dev.txt
python -m pip install --no-build-isolation -e '.[dev]'
python -m ruff check .
python -m ruff format --check .
python -c "import connectivity_support_agent"
python -m pip check
```

Ruff reported all checks passed and formatting unchanged. Import exited 0;
`pip check` found no broken requirements. Pytest was deliberately not run because
there are no meaningful behavioral tests in this foundation. Some sandboxed pip
commands disabled an unwritable shared cache; installation and checks succeeded.

### Sources verified

- [pytest metadata](https://pypi.org/project/pytest/)
- [Ruff metadata](https://pypi.org/project/ruff/)
- [setuptools metadata](https://pypi.org/project/setuptools/)
- [checkout v6.0.2](https://github.com/actions/checkout/releases/tag/v6.0.2)
- [setup-python v6.1.0](https://github.com/actions/setup-python/releases/tag/v6.1.0)

### Publishing and outstanding work

Local validation completed before staging. The initial baseline is authorized for
main; subsequent feature work requires a `codex/` branch and PR. Remote publication
and CI outcomes are recorded in the bootstrap delivery and any follow-up below;
this pre-publication entry does not assert that CI has run.

Next: implement the documented service-status core and Streamlit UI with meaningful
tests, add pytest to CI, and open a feature PR without merging or deploying.
Agent competencies remain unevaluated. A license decision remains with the owner.

Git initialization initially required sandbox escalation because `.git` is protected.
The authorized retry succeeded with `git init -b main`; explicit project paths
were staged and the complete staged diff and `git diff --cached --check` reviewed.
