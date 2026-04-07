import pysnow
from dotenv import load_dotenv
import os

load_dotenv()

def get_servicenow_client() -> pysnow.Client:
    return pysnow.Client(
        instance=os.getenv("SERVICENOW_INSTANCE_URL").replace("https://", "").replace(".service-now.com", ""),
        user=os.getenv("SERVICENOW_USERNAME"),
        password=os.getenv("SERVICENOW_PASSWORD"),
    )
