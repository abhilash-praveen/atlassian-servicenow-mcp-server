from atlassian import Confluence
from dotenv import load_dotenv
import os

load_dotenv()

def get_confluence_client() -> Confluence:
    return Confluence(
        url=os.getenv("JIRA_BASE_URL"),
        username=os.getenv("JIRA_EMAIL"),
        password=os.getenv("JIRA_API_TOKEN"),
        cloud=True,
    )
