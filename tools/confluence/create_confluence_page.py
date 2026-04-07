from clients.confluence_client import get_confluence_client
import os

def create_confluence_page(
    space_key: str,
    title: str,
    content: str,
    parent_id: str = None,
) -> dict:
    """Create a new Confluence page. Content should be in Confluence storage format (HTML-like)."""
    client = get_confluence_client()
    page = client.create_page(
        space=space_key,
        title=title,
        body=content,
        parent_id=parent_id,
        representation="storage",
    )
    return {
        "id": page["id"],
        "title": page["title"],
        "space_key": page["space"]["key"],
        "url": f"{os.getenv('JIRA_BASE_URL')}/wiki{page.get('_links', {}).get('webui', '')}",
    }
