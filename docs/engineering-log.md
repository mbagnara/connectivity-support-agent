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

## 2026-11-12 — Simulated service-status feature

### Inspection and implementation decisions

Read AGENTS.md, README, package configuration, requirements, CI, this log, and
learning progress. The checkout was clean on main at e3519e2, with the expected
GitHub origin. `git fetch origin` and `git merge --ff-only origin/main` confirmed
main was current, then `git switch -c codex/service-status` created the feature
branch. No unrelated changes were present or replaced.

Used `.venv/bin/python` for every Python install, check, test, and app run.
Verified `sys.executable` points to this repository's `.venv/bin/python`,
`sys.prefix` to the repository's `.venv`, and `sys.prefix != sys.base_prefix`.
Base prefix: `/opt/homebrew/opt/python@3.12/Frameworks/Python.framework/Versions/3.12`.
Interpreter remains CPython 3.12.14 on macOS ARM64; no host packages were installed.

Implemented the prescribed typed dictionary and deterministic messages in the
core, checking type before strip/casefold and rejecting blank input. Each call
constructs a fresh result. Streamlit is only imported by the root UI, which uses
a form, explicit submission, distinct status presentations, validation feedback,
and an expandable JSON view. No agent decisions or external service calls exist.

Official PyPI metadata verified Streamlit 1.67.0 requires Python >=3.11, compatible
with this environment. Checked official CLI, form, and AppTest API documentation:

- https://pypi.org/project/streamlit/
- https://docs.streamlit.io/get-started/installation/command-line
- https://docs.streamlit.io/develop/api-reference/execution-flow/st.form
- https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest

Added Streamlit to project dependencies using the existing exact-pin convention.
Captured resolved dependencies with `.venv/bin/python -m pip freeze --all
--exclude-editable`; all original foundation pins were preserved. Streamlit
metadata declares watchdog only off Darwin. Official PyPI metadata verified
watchdog 7.1.0 requires Python >=3.11; added it with that platform marker for Linux
CI reproducibility. Its Linux installation is validated by CI, not by macOS.

### Actual local validation

Successfully ran the supported installation sequence:

```sh
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pip install --no-build-isolation -e '.[dev]'
.venv/bin/python -m pip check
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m pytest
```

Used `.venv/bin/python -m ruff format .` to format new code before acceptance.
Dependency consistency and Ruff checks passed. Pytest passed 26 cases: 20 core
and 6 AppTest cases. Coverage includes fixtures, Unicode normalization, invalid
input types, blank inputs, deterministic calls, mutation isolation, initial UI
without results, all statuses, structured output, and validation after a result.
AppTest is simulated UI testing; no visual browser inspection was performed.

Startup initially failed because the sandbox prohibited binding a socket.
An authorized retry ran:

```sh
.venv/bin/python -m streamlit run app.py --server.headless=true --server.address=127.0.0.1 --server.port=8501 --browser.gatherUsageStats=false
```

Streamlit reported a running server at 127.0.0.1:8501. A local request using
`.venv/bin/python` to `/_stcore/health` returned HTTP 200 and `ok`. Stopped the
server after verification. This verifies startup/readiness, not browser rendering.
The user command is `.venv/bin/python -m streamlit run app.py`.

CI now runs pip check and the meaningful pytest suite alongside existing checks.
Publication and CI results will be reported in the feature delivery; this entry
records local evidence before publication. No merge or deployment is authorized.
Learner mastery remains unevaluated; review the implementation and understanding
before selecting further troubleshooting or agent work.

## 2026-11-12 — Troubleshooting-guide lookup

Inspected AGENTS.md, README, app, service core/tests, package configuration,
requirements, CI, and progress. Checkout was clean on main at merge commit
05a69b3 (PR #1). Verified origin, fetched, fast-forward synchronized main (already
current), and created codex/troubleshooting-guides. No unrelated changes existed.

Verified `.venv/bin/python` is the project executable, `sys.prefix` is the project
`.venv`, and it differs from the Homebrew Python 3.12 base prefix. Reused CPython
3.12.14 and existing package pins without installing or adding packages. Every
Python command used the project interpreter explicitly.

Implemented a private exact-identifier catalog with the supplied instructions
verbatim, stable step IDs, prescribed errors/messages, and fresh nested results.
The catalog is project-designed demonstration content, not an ISP manual or copied
book material. Added a separate guide form, keyed widgets and result containers,
placeholder validation, ordered steps, not-found warning, and structured output.
No agent routing, execution of checks, completion state, diagnosis, or external
calls were added. Existing service-status behavior is preserved.

Verified official Streamlit APIs for keyed containers, selectbox, and submit:
- https://docs.streamlit.io/develop/api-reference/layout/st.container
- https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox
- https://docs.streamlit.io/develop/api-reference/execution-flow/st.form_submit_button

Core tests cover all exact titles/instructions, order/IDs, known normalization,
Unicode casefold on unknown input, strict identifiers, errors, repeatability,
list mutation, and nested step mutation. AppTest retains service checks with
stable widget keys and scoped result queries; adds all guide selections,
placeholder validation, found-to-not-found cleanup, and boundary spies proving
forms call only their own tool. An initial spy test failed after a synthetic
intermediate AppTest rerun; corrected the test to select then submit as a form
interaction. The final full suite passes; no failed check is hidden by skipping.

Actual commands and outcomes:

```sh
.venv/bin/python -m ruff format .
.venv/bin/python -m pip check
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m pytest
```

Dependency consistency, lint, and format checks passed. All 56 tests passed
(20 service core, 25 guide core, 11 simulated UI cases). No API keys or external
services were needed. Existing CI already runs this entire suite; no workflow or
dependency changes were required.

Started the app using:

```sh
.venv/bin/python -m streamlit run app.py --server.headless=true --server.address=127.0.0.1 --server.port=8501 --browser.gatherUsageStats=false
```

The local server started; a request using `.venv/bin/python` to
`http://127.0.0.1:8501/_stcore/health` returned HTTP 200 `ok`. Stopped it afterward.
This verifies startup/readiness. AppTest is simulated UI testing, and no actual
browser inspection was performed. User command:
`.venv/bin/python -m streamlit run app.py`.

Updated README and learning progress. The learner's reported manual verification
of five first-feature cases and explanation of unknown versus outage are recorded
without extrapolating broader mastery. This feature's learner validation remains
pending. Publication and final CI observations are reported in the delivery.
No merge or deployment is authorized for this feature.
