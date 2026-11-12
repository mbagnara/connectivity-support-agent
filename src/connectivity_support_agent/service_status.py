"""Deterministic simulated service-status lookup, independent of the UI."""

from typing import Literal, TypedDict


class ServiceStatus(TypedDict):
    """Service evidence for a normalized zone; all data is simulated."""

    zone: str
    status: Literal["operational", "outage", "unknown"]
    message: str
    simulated: bool


def get_service_status(zone: str) -> ServiceStatus:
    """Return fresh simulated evidence, rejecting non-string or blank zones."""
    if not isinstance(zone, str):
        raise TypeError("Zone must be a string.")
    normalized_zone = zone.strip().casefold()
    if not normalized_zone:
        raise ValueError("Enter a nonempty zone.")

    status: Literal["operational", "outage", "unknown"]
    if normalized_zone == "north":
        status = "operational"
        message = "No service outage is reported for this zone."
    elif normalized_zone == "south":
        status = "outage"
        message = "A simulated service outage is reported for this zone."
    else:
        status = "unknown"
        message = "No service status information is available for this zone."
    return {
        "zone": normalized_zone,
        "status": status,
        "message": message,
        "simulated": True,
    }
