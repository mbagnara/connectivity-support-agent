# Connectivity Support Agent

An educational project exploring how a bounded support agent could handle internet
connectivity reports, consult simulated tools, and choose to answer, ask for
clarification, or simulate a human handoff.

## Current status

Foundation only: an importable Python package, pinned development dependencies,
engineering documentation, and CI checks. There is no runnable application,
service-status tool, Streamlit interface, model integration, or real service access.

## Setup and checks

Use Python 3.12 (bootstrap verified with CPython 3.12.14 on macOS ARM64).
The package requires Python 3.12 or later; other versions remain unverified.

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install --no-build-isolation -e '.[dev]'
python -m ruff check .
python -m ruff format --check .
python -c "import connectivity_support_agent"
```

The requirements file pins resolved development and build dependencies, including
pip. Install it before the editable package to reproduce the bootstrap environment.
`python -m pip install -e '.[dev]'` is also verified, but alone does not pin all
transitive dependencies. CI uses the pinned installation sequence above.
No tests exist yet; pytest is installed for the first feature. CI currently checks
installation, lint, formatting, and import only. See the engineering log for actual
local validation; a workflow file alone does not establish a successful CI run.

## Planned architecture and features

1. A deterministic service-status core tool, independently testable without UI.
2. A Streamlit interface calling that tool and displaying explicit simulation labels.
3. Simulated troubleshooting tools with explicit input/output contracts.
4. A bounded agent decision loop for answers, clarification, and simulated handoff.
5. Model integration and scenario evaluation once the core contracts are established.

The intended flow is user report → interface → decision loop → simulated tools →
structured evidence → answer, clarification, or simulated human handoff. These
components are planned, not implemented. Keep domain logic separate from UI and
any future model provider. Each feature gets a `codex/` branch and a separate PR;
feature PRs are not automatically merged or deployed.

## First feature contract (documentation only)

`get_service_status(zone: str)` will return a structured result containing:

| Field | Contract |
| --- | --- |
| `zone` | Input normalized with `strip()` then `casefold()` |
| `status` | `operational`, `outage`, or `unknown` |
| `message` | Concise English description consistent with status |
| `simulated` | Always `true` |

Fixed fixtures: `north` → `operational`; `south` → `outage`; any other nonempty
zone → `unknown`. Empty or whitespace input raises `ValueError`; non-string
input raises `TypeError`. Unknown must never be described as an outage. Use no
random data or fabricated restoration estimates.

The future UI accepts a zone, provides a **Check service** button, displays a
simulation notice and result or validation message, and can reveal the structured
result. The core tool must not depend on Streamlit. The first feature adds
Streamlit, meaningful pytest cases, and pytest execution in CI.

## Evaluation approach

Start with deterministic tests for fixtures, normalization (including casefold),
unknown zones, invalid types, empty input, and structured result consistency.
Check the UI's validation and simulation notice. Later evaluate scenarios covering
answer versus clarification versus handoff, tool evidence use, bounded execution,
and refusal to invent status or restoration estimates. Agent implementation
competencies remain unevaluated until implementation and evidence are reviewed.

## Limitations and attribution

All future service data and handoffs in this educational scope are simulated.
This project is not an ISP diagnostic system or a production support service.
No credentials are needed for the foundation. No license has been selected;
a licensing decision remains with the repository owner.

Conceptually adapted from *30 Agents Every AI Engineer Must Build*, chapter 5,
PDF pages 225–230, as identified in the project brief. The source pages were not
provided or inspected during bootstrap. No book text or code is reproduced, and
this is not an official implementation or an endorsed adaptation.

Codex AI assistance generated the initial scaffolding and documentation and ran
the recorded checks under the user's direction. Successful tool checks do not
establish learner mastery. See [learning progress](learning-progress.md) and the
[engineering log](docs/engineering-log.md).
