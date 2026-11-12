"""Behavioral contract tests for simulated service evidence."""

import pytest

from connectivity_support_agent.service_status import get_service_status


@pytest.mark.parametrize(
    ("zone", "status", "message"),
    [
        ("north", "operational", "No service outage is reported for this zone."),
        ("south", "outage", "A simulated service outage is reported for this zone."),
        (
            "east",
            "unknown",
            "No service status information is available for this zone.",
        ),
    ],
)
def test_fixture_results(zone, status, message):
    assert get_service_status(zone) == {
        "zone": zone,
        "status": status,
        "message": message,
        "simulated": True,
    }


@pytest.mark.parametrize(
    ("zone", "normalized"),
    [("  NORTH\t", "north"), ("\nSoUtH ", "south"), (" Straße ", "strasse")],
)
def test_normalization(zone, normalized):
    assert get_service_status(zone) == get_service_status(normalized)
    assert get_service_status(zone)["zone"] == normalized


@pytest.mark.parametrize("zone", ["", " ", "\t\n", "\u2003"])
def test_empty_zone_rejected(zone):
    with pytest.raises(ValueError):
        get_service_status(zone)


@pytest.mark.parametrize("zone", [None, 1, 1.5, True, b"north", [], {}])
def test_non_string_rejected(zone):
    with pytest.raises(TypeError):
        get_service_status(zone)


@pytest.mark.parametrize("zone", ["north", "south", "west"])
def test_repeated_calls_are_deterministic_and_isolated(zone):
    expected = get_service_status(zone)
    returned = get_service_status(zone)
    assert returned == expected
    returned.update(
        zone="corrupted", status="outage", message="changed", simulated=False
    )
    assert get_service_status(zone) == expected
