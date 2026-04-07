from clients.confluence_client import get_confluence_client

def list_confluence_spaces() -> list[dict]:
    """List all Confluence spaces accessible to the current user"""
    client = get_confluence_client()
    result = client.get_all_spaces(start=0, limit=50, expand="description.plain")
    spaces = []
    for space in result.get("results", []):
        spaces.append({
            "key": space["key"],
            "name": space["name"],
            "type": space["type"],
            "description": space.get("description", {}).get("plain", {}).get("value", ""),
        })
    return spaces
