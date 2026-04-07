from clients.servicenow_client import get_servicenow_client

_STATE_MAP = {"1": "New", "2": "In Progress", "3": "On Hold", "6": "Resolved", "7": "Closed"}
_URGENCY_MAP = {"1": "High", "2": "Medium", "3": "Low"}

def search_incidents(
    state: str = None,
    urgency: int = None,
    assigned_to: str = None,
    max_results: int = 10,
) -> list[dict]:
    """Search ServiceNow incidents by state and/or urgency.

    state: 'new', 'in_progress', 'on_hold', 'resolved', 'closed'
    urgency: 1=High, 2=Medium, 3=Low
    """
    _STATE_NAME_TO_NUM = {
        "new": "1", "in_progress": "2", "on_hold": "3", "resolved": "6", "closed": "7"
    }

    client = get_servicenow_client()
    query = {}
    if state:
        state_num = _STATE_NAME_TO_NUM.get(state.lower().replace(" ", "_"))
        if state_num:
            query["state"] = state_num
    if urgency:
        query["urgency"] = str(urgency)
    if assigned_to:
        query["assigned_to"] = assigned_to

    incidents = list(
        client.query(table="incident", query=query or {"active": "true"})
        .get_multiple(limit=max_results)
    )

    return [
        {
            "number": inc.get("number"),
            "short_description": inc.get("short_description"),
            "state": _STATE_MAP.get(str(inc.get("state")), inc.get("state")),
            "urgency": _URGENCY_MAP.get(str(inc.get("urgency")), inc.get("urgency")),
            "assigned_to": inc.get("assigned_to", {}).get("display_value") if isinstance(inc.get("assigned_to"), dict) else inc.get("assigned_to"),
            "opened_at": inc.get("opened_at"),
        }
        for inc in incidents
    ]
