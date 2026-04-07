from clients.servicenow_client import get_servicenow_client

def create_incident(
    short_description: str,
    description: str = None,
    urgency: int = 3,
    impact: int = 3,
    caller_id: str = None,
) -> dict:
    """Create a new ServiceNow incident.

    urgency/impact: 1=High, 2=Medium, 3=Low
    """
    client = get_servicenow_client()
    payload = {
        "short_description": short_description,
        "urgency": urgency,
        "impact": impact,
    }
    if description:
        payload["description"] = description
    if caller_id:
        payload["caller_id"] = caller_id

    result = client.insert(table="incident", payload=payload)
    return {
        "number": result.get("number"),
        "sys_id": result.get("sys_id"),
        "short_description": result.get("short_description"),
        "state": result.get("state"),
        "urgency": result.get("urgency"),
        "impact": result.get("impact"),
    }
