from jira_client import get_jira_client

def add_jira_comment(issue_id: str, body: str) -> dict:
    """Add a comment to a Jira issue"""
    client = get_jira_client()
    comment = client.add_comment(issue_id, body)
    return {
        "id": comment.id,
        "issue_id": issue_id,
        "body": comment.body,
        "author": comment.author.displayName,
    }
