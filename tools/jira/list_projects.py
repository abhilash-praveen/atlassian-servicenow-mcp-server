from clients.jira_client import get_jira_client

def list_jira_projects() -> list[dict]:
    """List all Jira projects accessible to the current user"""
    client = get_jira_client()
    projects = client.projects()
    return [
        {
            "key": project.key,
            "name": project.name,
            "id": project.id,
        }
        for project in projects
    ]
