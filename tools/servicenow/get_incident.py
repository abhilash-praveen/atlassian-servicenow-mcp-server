from clients.servicenow_client import get_servicenow_client

_STATE_MAP = {"1": "New", "2": "In Progress", "3": "On Hold", "6": "Resolved", "7": "Closed"}
_URGENCY_MAP = {"1": "High", "2": "Medium", "3": "Low"}
_IMPACT_MAP = {"1": "High", "2": "Medium", "3": "Low"}

def get_incident(number: str) -> dict:
    """Get a ServiceNow incident by its number (e.g. INC0010001)"""
    client = get_servicenow_client()
    inc = client.query(table="incident", query={"number": number}).get_one()
    if not inc:
        return {"error": f"Incident {number} not found"}
    return {
        "number": inc.get("number"),
        "sys_id": inc.get("sys_id"),
        "short_description": inc.get("short_description"),
        "description": inc.get("description"),
        "state": _STATE_MAP.get(str(inc.get("state")), inc.get("state")),
        "urgency": _URGENCY_MAP.get(str(inc.get("urgency")), inc.get("urgency")),
        "impact": _IMPACT_MAP.get(str(inc.get("impact")), inc.get("impact")),
        "assigned_to": inc.get("assigned_to", {}).get("display_value") if isinstance(inc.get("assigned_to"), dict) else inc.get("assigned_to"),
        "opened_at": inc.get("opened_at"),
        "resolved_at": inc.get("resolved_at"),
    }
