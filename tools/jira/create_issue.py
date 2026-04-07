from clients.jira_client import get_jira_client
from dotenv import load_dotenv
import os

load_dotenv()

def create_jira_issue(project_key: str, summary: str, description: str, issue_type: str = "Task") -> dict:
    """Create a new Jira issue"""
    client = get_jira_client()
    issue = client.create_issue(fields={
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
    })
    return {
        "id": issue.key,
        "summary": issue.fields.summary,
        "url": f"{os.getenv('JIRA_BASE_URL')}/browse/{issue.key}"
    }