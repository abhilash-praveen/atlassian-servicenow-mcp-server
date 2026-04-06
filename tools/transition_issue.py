from jira_client import get_jira_client

def transition_jira_issue(issue_id: str, transition_name: str) -> dict:
    """Transition a Jira issue to a new status (e.g. 'In Progress', 'Done')"""
    client = get_jira_client()
    transitions = client.transitions(issue_id)
    match = next((t for t in transitions if t["name"].lower() == transition_name.lower()), None)
    if not match:
        available = [t["name"] for t in transitions]
        raise ValueError(f"Transition '{transition_name}' not found. Available: {available}")
    client.transition_issue(issue_id, match["id"])
    issue = client.issue(issue_id)
    return {
        "id": issue.key,
        "status": issue.fields.status.name,
    }
