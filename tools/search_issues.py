from jira_client import get_jira_client

def search_jira_issues(jql: str, max_results: int = 10) -> list[dict]:
    """Search Jira issues using a JQL query"""
    client = get_jira_client()
    issues = client.search_issues(jql, maxResults=max_results)
    return [
        {
            "id": issue.key,
            "summary": issue.fields.summary,
            "status": issue.fields.status.name,
            "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
        }
        for issue in issues
    ]