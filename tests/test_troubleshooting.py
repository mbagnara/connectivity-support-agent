"""Public guide contract and exact educational catalog expectations."""

import pytest

from connectivity_support_agent.troubleshooting import get_troubleshooting_guide

GUIDES = [
    (
        "wifi_unavailable",
        "Cannot connect to Wi-Fi",
        [
            "Check whether Wi-Fi is enabled on the affected device.",
            "Check whether your expected network appears in the available networks list.",
            "Check whether another device can see and connect to the same network, and note the result.",
        ],
    ),
    (
        "connected_no_internet",
        "Connected without internet access",
        [
            "Confirm that the device is connected to the intended network.",
            "Check whether another website or application has the same connectivity problem.",
            "Check whether another device on the same network has internet access, and note the result.",
        ],
    ),
    (
        "slow_connection",
        "Slow connection",
        [
            "Check whether the slowdown affects one application or several applications.",
            "Check whether another device on the same network experiences the slowdown.",
            "If using Wi-Fi, compare connectivity closer to the router and note any change.",
        ],
    ),
]


@pytest.mark.parametrize(("symptom", "title", "instructions"), GUIDES)
def test_exact_catalog(symptom, title, instructions):
    assert get_troubleshooting_guide(symptom) == {
        "symptom": symptom,
        "status": "found",
        "title": title,
        "steps": [
            {"id": f"step_{i}", "instruction": text}
            for i, text in enumerate(instructions, 1)
        ],
        "message": "Follow these demonstration checks and report what you observe. They do not establish a diagnosis.",
        "simulated": True,
    }


@pytest.mark.parametrize(
    "symptom", ["other", "Cannot connect to Wi-Fi", "wifi unavailable", " Straße "]
)
def test_unknown_has_no_steps_or_diagnosis(symptom):
    assert get_troubleshooting_guide(symptom) == {
        "symptom": symptom.strip().casefold(),
        "status": "not_found",
        "title": "No guide available",
        "steps": [],
        "message": "No troubleshooting guide is available for this symptom.",
        "simulated": True,
    }


@pytest.mark.parametrize("symptom", [row[0] for row in GUIDES])
def test_normalization_and_repeatability(symptom):
    assert get_troubleshooting_guide(
        f" \t{symptom.upper()}\n"
    ) == get_troubleshooting_guide(symptom)
    assert get_troubleshooting_guide(symptom) == get_troubleshooting_guide(symptom)


@pytest.mark.parametrize("symptom", ["", " ", "\t\n", "\u2003"])
def test_blank_rejected(symptom):
    with pytest.raises(ValueError, match="^Enter a nonempty symptom\\.$"):
        get_troubleshooting_guide(symptom)


@pytest.mark.parametrize("symptom", [None, True, 1, 1.5, b"wifi_unavailable", [], {}])
def test_invalid_type_rejected(symptom):
    with pytest.raises(TypeError, match="^Symptom must be a string\\.$"):
        get_troubleshooting_guide(symptom)


@pytest.mark.parametrize("symptom", [row[0] for row in GUIDES])
def test_list_and_nested_step_mutation_isolation(symptom):
    expected = get_troubleshooting_guide(symptom)
    changed = get_troubleshooting_guide(symptom)
    changed["steps"][0]["instruction"] = "corrupted"
    changed["steps"][0]["id"] = "changed"
    assert get_troubleshooting_guide(symptom) == expected
    changed["steps"].clear()
    changed["steps"].append({"id": "extra", "instruction": "extra"})
    assert get_troubleshooting_guide(symptom) == expected


def test_unknown_list_is_fresh():
    result = get_troubleshooting_guide("other")
    result["steps"].append({"id": "extra", "instruction": "extra"})
    assert get_troubleshooting_guide("other")["steps"] == []
