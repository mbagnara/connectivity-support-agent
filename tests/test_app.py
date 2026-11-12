"""Simulated UI integration using Streamlit AppTest; no browser required."""

import json
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def test_initial_state_has_no_lookup_result():
    app = AppTest.from_file(str(APP)).run()
    assert not app.exception
    assert app.title[0].value == "Connectivity Support Agent"
    assert "Simulated service data" in app.info[0].value
    assert "not yet an AI agent" in app.info[0].value
    assert not app.success and not app.error and not app.warning and not app.json
    app.text_input[0].set_value("north").run()
    assert not app.json and not app.success


@pytest.mark.parametrize(
    ("zone", "element", "status", "message"),
    [
        (
            " NORTH ",
            "success",
            "operational",
            "No service outage is reported for this zone.",
        ),
        (
            "south",
            "error",
            "outage",
            "A simulated service outage is reported for this zone.",
        ),
        (
            "east",
            "warning",
            "unknown",
            "No service status information is available for this zone.",
        ),
    ],
)
def test_submitted_result(zone, element, status, message):
    app = AppTest.from_file(str(APP)).run()
    app.text_input[0].set_value(zone)
    app.button[0].click().run()
    assert not app.exception
    assert app.get(element)[0].value == f"{status.capitalize()}: {message}"
    assert len(app.success) + len(app.error) + len(app.warning) == 1
    assert app.expander[0].label == "Structured result"
    assert json.loads(app.json[0].value) == {
        "zone": zone.strip().casefold(),
        "status": status,
        "message": message,
        "simulated": True,
    }
    app.text_input[0].set_value("   ")
    app.button[0].click().run()
    assert not app.exception
    assert app.error[0].value == "Enter a nonempty zone."
    assert not app.json and not app.success and not app.warning


@pytest.mark.parametrize("zone", ["", "  \t"])
def test_blank_submission_shows_validation(zone):
    app = AppTest.from_file(str(APP)).run()
    app.text_input[0].set_value(zone)
    app.button[0].click().run()
    assert not app.exception
    assert app.error[0].value == "Enter a nonempty zone."
    assert not app.json
