# Learning progress

## Foundation — 2026-11-12

The learner knows Python. Agent implementation competencies remain unevaluated.
AI-assisted scaffolding and successful environment checks are not evidence of
independent mastery. No agent behavior has been implemented or assessed.

Current artifacts: minimal importable package, development dependency pins, Ruff
configuration, CI workflow, and engineering documentation. See the engineering log
for validation outcomes and publishing state.

## Next feature

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

The first-feature plan above is now implemented and awaiting PR review. Next,
review this feature and assess understanding before choosing a follow-up feature;
troubleshooting tools and bounded agent integration remain planned. Do not merge
or deploy automatically.
