from clients.confluence_client import get_confluence_client
import os

def search_confluence(query: str, max_results: int = 10) -> list[dict]:
    """Search Confluence pages using a CQL query (e.g. 'text ~ "deployment" AND space = "ENG"')"""
    client = get_confluence_client()
    results = client.cql(query, limit=max_results, expand="space")
    pages = []
    for result in results.get("results", []):
        content = result.get("content")
        if not content:
            continue
        pages.append({
            "id": content["id"],
            "title": content["title"],
            "type": content["type"],
            "space_key": result["resultGlobalContainer"]["title"] if "resultGlobalContainer" in result else None,
            "url": f"{os.getenv('JIRA_BASE_URL')}/wiki{result.get('url', '')}",
            "excerpt": result.get("excerpt", ""),
        })
    return pages
