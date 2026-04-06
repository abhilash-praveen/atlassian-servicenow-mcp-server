from fastmcp import FastMCP
from tools.get_issue import get_jira_issue
from tools.search_issues import search_jira_issues
from tools.create_issue import create_jira_issue
from tools.transition_issue import transition_jira_issue
from tools.update_issue import update_jira_issue
from tools.add_comment import add_jira_comment
from tools.list_projects import list_jira_projects

mcp = FastMCP("Jira MCP Server")

mcp.tool()(get_jira_issue)
mcp.tool()(search_jira_issues)
mcp.tool()(create_jira_issue)
mcp.tool()(transition_jira_issue)
mcp.tool()(update_jira_issue)
mcp.tool()(add_jira_comment)
mcp.tool()(list_jira_projects)

if __name__ == "__main__":
    mcp.run()