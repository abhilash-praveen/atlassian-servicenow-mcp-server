from fastmcp import FastMCP
from tools.jira.get_issue import get_jira_issue
from tools.jira.search_issues import search_jira_issues
from tools.jira.create_issue import create_jira_issue
from tools.jira.transition_issue import transition_jira_issue
from tools.jira.update_issue import update_jira_issue
from tools.jira.add_comment import add_jira_comment
from tools.jira.list_projects import list_jira_projects
from tools.confluence.get_confluence_page import get_confluence_page
from tools.confluence.search_confluence import search_confluence
from tools.confluence.create_confluence_page import create_confluence_page
from tools.confluence.list_confluence_spaces import list_confluence_spaces

mcp = FastMCP("Jira & Confluence MCP Server")

mcp.tool()(get_jira_issue)
mcp.tool()(search_jira_issues)
mcp.tool()(create_jira_issue)
mcp.tool()(transition_jira_issue)
mcp.tool()(update_jira_issue)
mcp.tool()(add_jira_comment)
mcp.tool()(list_jira_projects)

mcp.tool()(get_confluence_page)
mcp.tool()(search_confluence)
mcp.tool()(create_confluence_page)
mcp.tool()(list_confluence_spaces)

if __name__ == "__main__":
    mcp.run()