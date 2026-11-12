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
    assert (
        not app.get_by_key("service_result").success
        and not app.get_by_key("service_result").error
        and not app.get_by_key("service_result").warning
        and not app.get_by_key("service_result").json
    )
    app.text_input(key="service_zone").set_value("north").run()
    assert (
        not app.get_by_key("service_result").json
        and not app.get_by_key("service_result").success
    )


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
    app.text_input(key="service_zone").set_value(zone)
    app.button(key="service_submit").click().run()
    assert not app.exception
    assert (
        app.get_by_key("service_result").get(element)[0].value
        == f"{status.capitalize()}: {message}"
    )
    assert (
        len(app.get_by_key("service_result").success)
        + len(app.get_by_key("service_result").error)
        + len(app.get_by_key("service_result").warning)
        == 1
    )
    assert app.get_by_key("service_result").expander[0].label == "Structured result"
    assert json.loads(app.get_by_key("service_result").json[0].value) == {
        "zone": zone.strip().casefold(),
        "status": status,
        "message": message,
        "simulated": True,
    }
    app.text_input(key="service_zone").set_value("   ")
    app.button(key="service_submit").click().run()
    assert not app.exception
    assert app.get_by_key("service_result").error[0].value == "Enter a nonempty zone."
    assert (
        not app.get_by_key("service_result").json
        and not app.get_by_key("service_result").success
        and not app.get_by_key("service_result").warning
    )


@pytest.mark.parametrize("zone", ["", "  \t"])
def test_blank_submission_shows_validation(zone):
    app = AppTest.from_file(str(APP)).run()
    app.text_input(key="service_zone").set_value(zone)
    app.button(key="service_submit").click().run()
    assert not app.exception
    assert app.get_by_key("service_result").error[0].value == "Enter a nonempty zone."
    assert not app.get_by_key("service_result").json


@pytest.mark.parametrize(
    ("label", "identifier"),
    [
        ("Cannot connect to Wi-Fi", "wifi_unavailable"),
        ("Connected without internet access", "connected_no_internet"),
        ("Slow connection", "slow_connection"),
    ],
)
def test_known_guide(label, identifier):
    from connectivity_support_agent.troubleshooting import get_troubleshooting_guide

    app = AppTest.from_file(str(APP)).run()
    app.selectbox(key="guide_symptom").select(label)
    app.button(key="guide_submit").click().run()
    assert not app.exception
    expected = get_troubleshooting_guide(identifier)
    scope = app.get_by_key("guide_result")
    assert scope.subheader[0].value == expected["title"]
    assert scope.markdown[0].value == expected["message"]
    assert scope.markdown[1].value == "\n".join(
        f"{i}. {step['instruction']}" for i, step in enumerate(expected["steps"], 1)
    )
    assert scope.expander[0].label == "Guide structured result"
    assert json.loads(scope.json[0].value) == expected
    app.selectbox(key="guide_symptom").select("Other symptom")
    app.button(key="guide_submit").click().run()
    assert not app.exception
    scope = app.get_by_key("guide_result")
    assert not scope.subheader and not scope.markdown
    assert (
        scope.warning[0].value
        == "No troubleshooting guide is available for this symptom."
    )
    assert json.loads(scope.json[0].value)["steps"] == []


def test_placeholder_validation_and_no_initial_guide():
    app = AppTest.from_file(str(APP)).run()
    assert not app.get_by_key("guide_result").json
    assert app.selectbox(key="guide_symptom").options == [
        "Select a symptom",
        "Cannot connect to Wi-Fi",
        "Connected without internet access",
        "Slow connection",
        "Other symptom",
    ]
    app.button(key="guide_submit").click().run()
    assert not app.exception
    scope = app.get_by_key("guide_result")
    assert scope.error[0].value == "Select a symptom."
    assert not scope.json and not scope.markdown


def test_forms_only_call_their_own_tool(monkeypatch):
    import importlib

    service_status = importlib.import_module(
        "connectivity_support_agent.service_status"
    )
    troubleshooting = importlib.import_module(
        "connectivity_support_agent.troubleshooting"
    )

    service_calls = []
    guide_calls = []
    original_service = service_status.get_service_status
    original_guide = troubleshooting.get_troubleshooting_guide

    def service_spy(zone):
        service_calls.append(zone)
        return original_service(zone)

    def guide_spy(symptom):
        guide_calls.append(symptom)
        return original_guide(symptom)

    monkeypatch.setattr(service_status, "get_service_status", service_spy)
    monkeypatch.setattr(troubleshooting, "get_troubleshooting_guide", guide_spy)
    app = AppTest.from_file(str(APP)).run()
    assert not service_calls and not guide_calls
    app.selectbox(key="guide_symptom").select("Slow connection")
    assert not service_calls and not guide_calls
    app.button(key="guide_submit").click().run()
    assert not app.exception
    assert guide_calls == ["slow_connection"]
    assert not service_calls
    app.text_input(key="service_zone").set_value("north")
    app.button(key="service_submit").click().run()
    assert not app.exception
    assert service_calls == ["north"]
    assert guide_calls == ["slow_connection"]
