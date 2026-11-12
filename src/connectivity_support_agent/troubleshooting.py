"""Project-designed demonstration guides, retrieved by exact symptom identifier."""

from typing import Literal, TypedDict


class TroubleshootingStep(TypedDict):
    """One stable, ordered demonstration check."""

    id: str
    instruction: str


class TroubleshootingGuide(TypedDict):
    """Simulated guidance, not an executed check or diagnosis."""

    symptom: str
    status: Literal["found", "not_found"]
    title: str
    steps: list[TroubleshootingStep]
    message: str
    simulated: bool


_CATALOG = {
    "wifi_unavailable": (
        "Cannot connect to Wi-Fi",
        (
            "Check whether Wi-Fi is enabled on the affected device.",
            "Check whether your expected network appears in the available networks list.",
            "Check whether another device can see and connect to the same network, and note the result.",
        ),
    ),
    "connected_no_internet": (
        "Connected without internet access",
        (
            "Confirm that the device is connected to the intended network.",
            "Check whether another website or application has the same connectivity problem.",
            "Check whether another device on the same network has internet access, and note the result.",
        ),
    ),
    "slow_connection": (
        "Slow connection",
        (
            "Check whether the slowdown affects one application or several applications.",
            "Check whether another device on the same network experiences the slowdown.",
            "If using Wi-Fi, compare connectivity closer to the router and note any change.",
        ),
    ),
}


def get_troubleshooting_guide(symptom: str) -> TroubleshootingGuide:
    """Retrieve an exact identifier; future agents must map user descriptions."""
    if not isinstance(symptom, str):
        raise TypeError("Symptom must be a string.")
    normalized = symptom.strip().casefold()
    if not normalized:
        raise ValueError("Enter a nonempty symptom.")

    entry = _CATALOG.get(normalized)
    if entry is None:
        return {
            "symptom": normalized,
            "status": "not_found",
            "title": "No guide available",
            "steps": [],
            "message": "No troubleshooting guide is available for this symptom.",
            "simulated": True,
        }
    title, instructions = entry
    return {
        "symptom": normalized,
        "status": "found",
        "title": title,
        "steps": [
            {"id": f"step_{index}", "instruction": instruction}
            for index, instruction in enumerate(instructions, start=1)
        ],
        "message": (
            "Follow these demonstration checks and report what you observe. "
            "They do not establish a diagnosis."
        ),
        "simulated": True,
    }
