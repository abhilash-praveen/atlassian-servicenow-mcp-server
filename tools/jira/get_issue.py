from clients.jira_client import get_jira_client

def get_jira_issue(issue_id: str) -> dict:
    """Get a Jira issue by its ID (e.g. PROJ-123)"""
    client = get_jira_client()
    issue = client.issue(issue_id)
    return {
        "id": issue.key,
        "summary": issue.fields.summary,
        "status": issue.fields.status.name,
        "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
        "description": issue.fields.description,
    }