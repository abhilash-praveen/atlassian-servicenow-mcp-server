from clients.confluence_client import get_confluence_client
import os

def get_confluence_page(page_id: str) -> dict:
    """Get a Confluence page by its ID"""
    client = get_confluence_client()
    page = client.get_page_by_id(page_id, expand="body.storage,version,space")
    return {
        "id": page["id"],
        "title": page["title"],
        "space_key": page["space"]["key"],
        "space_name": page["space"]["name"],
        "version": page["version"]["number"],
        "content": page["body"]["storage"]["value"],
        "url": f"{os.getenv('JIRA_BASE_URL')}/wiki{page.get('_links', {}).get('webui', '')}",
    }
