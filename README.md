# Connectivity Support Agent

An educational project exploring how a bounded support agent could handle internet
connectivity reports, consult simulated tools, and choose to answer, ask for
clarification, or simulate a human handoff.

## Current status

Deterministic service-status and troubleshooting-guide tools are implemented in
a Streamlit UI as independent demonstrations. Model integration is not implemented.
There is no agent routing, real service coverage, diagnosis, or human handoff.

## Isolated setup and checks

Use Python 3.12 (verified with CPython 3.12.14 on macOS ARM64).
The package requires Python 3.12 or later; other versions remain unverified.
Create the environment once, then use its interpreter explicitly:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pip install --no-build-isolation -e '.[dev]'
.venv/bin/python -m pip check
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m pytest
.venv/bin/python -c "import connectivity_support_agent"
```

The requirements file preserves the foundation pins and adds Streamlit 1.67.0 and
its resolved dependencies, including a non-macOS watchdog pin for Linux CI.
CI checks installation, dependency consistency, lint, formatting, package import,
and the meaningful core and simulated UI test suite. No API keys, paid services,
or external service calls are needed to run checks or use the tool.

## Try the UI on macOS

```sh
.venv/bin/python -m streamlit run app.py
```

Enter ` NORTH ` and click **Check service** to see **Operational: No service outage
is reported for this zone.** Expand **Structured result** to inspect the normalized
zone, status, message, and simulation flag. Nothing is looked up before submission.
Blank input shows validation feedback. Unknown status is separate from outage.

## Architecture and planned features

1. Implemented: deterministic service-status core, independently testable without UI.
2. Implemented: Streamlit form calling the core with explicit simulation labels.
3. Implemented: deterministic troubleshooting-guide retrieval with typed outputs.
4. A bounded agent decision loop for answers, clarification, and simulated handoff.
5. Model integration and scenario evaluation once the core contracts are established.

The intended flow is user report → interface → decision loop → simulated tools →
structured evidence → answer, clarification, or simulated human handoff. The
decision loop remains planned. Keep domain logic separate
from UI and any future model provider. Each feature gets a `codex/` branch and a separate PR;
feature PRs are not automatically merged or deployed.

## Service-status contract

`get_service_status(zone: str)` in `connectivity_support_agent.service_status`
returns a fresh `ServiceStatus` typed dictionary containing:

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

The UI accepts a zone, provides a **Check service** button, displays a
simulation notice and result or validation message, and can reveal the structured
result. The core tool does not depend on Streamlit. Operational status does not
establish a local device fault. No restoration estimates or real coverage are inferred.

## Troubleshooting-guide lookup

In **Troubleshooting guides**, select a symptom and click **Get troubleshooting
guide**. **Cannot connect to Wi-Fi**, **Connected without internet access**, and
**Slow connection** show an educational message and three ordered checks.
**Other symptom** returns a warning with no steps. The placeholder shows
**Select a symptom.** without calling the tool. Expand **Guide structured result**
to inspect JSON. Both forms work independently; submitting one calls only its own
tool. Results are scoped to the current submission, with no diagnostic history.

`get_troubleshooting_guide(symptom: str)` in
`connectivity_support_agent.troubleshooting` accepts exact identifiers, normalizing
with `strip().casefold()`. It does not interpret natural-language descriptions or
use fuzzy matching. Non-string input raises `TypeError("Symptom must be a string.")`;
blank input raises `ValueError("Enter a nonempty symptom.")`.

| Identifier | Guide title |
| --- | --- |
| `wifi_unavailable` | Cannot connect to Wi-Fi |
| `connected_no_internet` | Connected without internet access |
| `slow_connection` | Slow connection |

The returned `TroubleshootingGuide` has normalized `symptom`, `status` (`found` or
`not_found`), `title`, `steps`, `message`, and `simulated=True`. Each step has a
stable `id` (`step_1` through `step_3`) and an `instruction`. Each call returns a
fresh list and step dictionaries. Unknown identifiers (including the UI's `other`)
return `not_found`, title **No guide available**, no steps, and **No troubleshooting
guide is available for this symptom.** Known guides state: **Follow these
demonstration checks and report what you observe. They do not establish a diagnosis.**

This is a project-designed demonstration catalog, not a verified ISP manual or
verbatim book content. The tool retrieves instructions; it does not execute checks,
track completion, diagnose devices, or establish resolution. It performs no resets,
credential collection, external calls, random generation, or automatic handoff.
A future agent must choose the tool and map a user's description to valid arguments;
that responsibility is not implemented in these independent UI demonstrations.

## Evaluation approach

The suite covers fixtures, normalization (including Unicode casefold), unknown
zones, invalid types, empty input, repeatability, and mutation isolation. Streamlit
AppTest simulates initial state, all three statuses, structured output, and blank
validation. Guide tests verify exact ordered catalog content, input validation,
repeatability, nested mutation isolation, selection mapping, not-found transitions
without stale steps, and independent tool calls. This is simulated UI testing,
not visual browser inspection. Later
evaluate scenarios covering
answer versus clarification versus handoff, tool evidence use, bounded execution,
and refusal to invent status or restoration estimates. Agent implementation
competencies remain unevaluated until implementation and evidence are reviewed.

## Limitations and attribution

All service data is simulated. Future handoffs in this educational scope will
also be simulated.
This project is not an ISP diagnostic system or a production support service.
No credentials are needed for this feature. No license has been selected;
a licensing decision remains with the repository owner.

Conceptually adapted from *30 Agents Every AI Engineer Must Build*, chapter 5,
PDF pages 225–230, as identified in the project brief. The source pages were not
provided or inspected during bootstrap. No book text or code is reproduced, and
this is not an official implementation or an endorsed adaptation.

Codex AI assistance generated the scaffolding, lookup implementation, tests, and
documentation and ran the recorded checks under the user's direction. Successful tool checks do not
establish learner mastery. See [learning progress](learning-progress.md) and the
[engineering log](docs/engineering-log.md).
