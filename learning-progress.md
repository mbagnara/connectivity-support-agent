# Learning progress

## Foundation — 2026-11-12

The learner knows Python. Agent implementation competencies remain unevaluated.
AI-assisted scaffolding and successful environment checks are not evidence of
independent mastery. No agent behavior has been implemented or assessed.

Current artifacts: minimal importable package, development dependency pins, Ruff
configuration, CI workflow, and engineering documentation. See the engineering log
for validation outcomes and publishing state.

## Historical first-feature plan

On `codex/service-status`, implement the documented deterministic
`get_service_status(zone: str)` contract, meaningful tests, and a Streamlit UI.
Add pytest execution to CI with those tests. Open a feature PR; do not merge it
or deploy. Review the learner's explanation of normalization, validation,
structured outputs, simulation boundaries, and separation of core logic from UI.
Later evaluate tool selection, decision loops, clarification, and handoff behavior.

## Service-status feature — 2026-11-12

Implemented on `codex/service-status`: deterministic core tool, Streamlit lookup
form, pinned dependencies, and core/AppTest integration tests. Local acceptance
checks passed with 26 test cases (20 core and 6 simulated UI cases). Agent behavior
has not been implemented. Generated code and passing checks do not establish
learner mastery; normalization, validation, mutation isolation, and UI separation
still require learner explanation and independent implementation assessment.

The first feature was merged in PR #1, verified on main at 05a69b3. The learner
reports manually verifying its five cases and explained why unknown differs from
outage. This evidence does not establish broader agent implementation mastery.


## Troubleshooting guides — 2026-11-12

Implemented exact-identifier guide retrieval, three demonstration guides, typed
outputs with fresh nested data, and an independent Streamlit form. Automated
validation passed 56 cases across both core tools and simulated UI integration.
Learner manual validation and explanation of this feature are pending. Generated
implementation and passing tests do not establish mastery. Agent tool selection,
argument mapping, bounded execution, and handoff remain unimplemented and
unevaluated. Review this feature before selecting further work; do not merge or
deploy automatically.
