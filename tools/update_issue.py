from jira_client import get_jira_client

def update_jira_issue(issue_id: str, summary: str = None, description: str = None, priority: str = None, labels: list[str] = None) -> dict:
    """Update fields on an existing Jira issue"""
    client = get_jira_client()
    fields = {}
    if summary is not None:
        fields["summary"] = summary
    if description is not None:
        fields["description"] = description
    if priority is not None:
        fields["priority"] = {"name": priority}
    if labels is not None:
        fields["labels"] = labels
    client.issue(issue_id).update(fields=fields)
    issue = client.issue(issue_id)
    return {
        "id": issue.key,
        "summary": issue.fields.summary,
        "status": issue.fields.status.name,
    }
