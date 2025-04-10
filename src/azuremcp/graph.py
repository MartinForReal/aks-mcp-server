from context import app_lifespan

from pydantic import Field
from mcp.server.fastmcp import Context, FastMCP
from azure.mgmt.resourcegraph.aio import ResourceGraphClient

# Constants
USER_AGENT = "azure-graph-mcp-server/1.0"

# Initialize FastMCP server
azureGraph = FastMCP(
    "Azure graph service MCP server",
    "This mcp server will send query to Azure graph service and it will return azure resource profile in json format",
    dependencies=["azure-mgmt-resourcegraph", "azure-identity", "aiohttp"],
    lifespan=app_lifespan,
)

@azureGraph.tool(
    name="Search azure graph service",
    description="Get azure profile in json format from azure rest graph service, send azure resource graph query to azure graph service and return the result in json format.",
)
async def get_azure_resource_profile(
    ctx: Context,
    query: str = Field(
        description="Azure resource graph query to be sent to azure graph service.",
    ),
) -> list:
    """
    Azure graph service 
    Args:

    Returns:
            str: The Azure resource profile in JSON format.
    """
    result = None
    async with ResourceGraphClient(
        credential=ctx.request_context.lifespan_context.credential,
        user_agent=USER_AGENT,
    ) as client:
        result = await client.resources(
			query=query,
		)
        await client.close()
    
    data = list()
    for item in result.data:
        data.append(item)
    return data