from jira import JIRA
from dotenv import load_dotenv
import os

load_dotenv()

def get_jira_client() -> JIRA:
    return JIRA(
        server=os.getenv("JIRA_BASE_URL"),
        basic_auth=(
            os.getenv("JIRA_EMAIL"),
            os.getenv("JIRA_API_TOKEN")
        )
    )