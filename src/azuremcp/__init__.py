from mcp.server.fastmcp import FastMCP
from containerservice import managedCluster
from network import virtualNetwork, routeTable, securityGroup, natGateway, loadBalancer
from resource import resourceGroup
from graph import azureGraph
from context import app_lifespan


server = FastMCP(
    "Azure resource rest api MCP server",
    lifespan=app_lifespan,
)
for mcpInstance in [managedCluster, virtualNetwork, routeTable, resourceGroup, securityGroup, natGateway, loadBalancer, azureGraph]:
    server.dependencies = list(
        set(server.dependencies).union(mcpInstance.dependencies))
    for tool in mcpInstance._tool_manager.list_tools():
        server.add_tool(tool.fn, tool.name, tool.description)
    for prompt in mcpInstance._prompt_manager.list_prompts():
        server.add_prompt(prompt)
    for resource in mcpInstance._resource_manager.list_resources():
        server._resource_manager.add_resource(resource)
    for template in mcpInstance._resource_manager.list_templates():
        server._resource_manager.add_template(template)

__all__ = ["virtualNetwork", "managedCluster", "routeTable",
           "resourceGroup", "securityGroup", "natGateway", "loadBalancer", "azureGraph"]
