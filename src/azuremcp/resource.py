from context import app_lifespan

from pydantic import Field
from mcp.server.fastmcp import Context, FastMCP
from azure.mgmt.resource.resources.aio import ResourceManagementClient

# Constants
USER_AGENT = "azure-resource-mcp-server/1.0"

# Initialize FastMCP server
resourceGroup = FastMCP(
    "Azure resource group MCP server",
    "This mcp server will operate on Azure resource group.Put subscriptionid, and resource group name and get the list of azure resources.",
    dependencies=["azure-mgmt-resource", "azure-identity", "aiohttp"],
    lifespan=app_lifespan,
)

@resourceGroup.tool(
    name="Get-Azure-resource-Profile",
    description="Get Azure resource group profile in JSON format from azure rest api."
    "SubscriptionId, resourceGroupName are required parameters. "
    "It returns the azure resource group profile in JSON format. "
    "The profile spec can be found here: https://learn.microsoft.com/en-us/rest/api/resources/resource-groups/get",
)
async def get_azure_resource_group(
    ctx: Context,
    subscriptionId: str = Field(description="The Azure subscription ID."),
    resourceGroupName: str = Field(description="The Azure resource group name."),
) -> bytes:
    """
    Azure resource group profile.
    Args:
            subscriptionId (str): The Azure subscription ID.
            resourceGroupName (str): The Azure resource group name.
    Returns:
            str: The resource group profile in JSON format.
    """
    rg = None
    async with ResourceManagementClient(
        credential=ctx.request_context.lifespan_context.credential,
        subscription_id=subscriptionId,
        user_agent=USER_AGENT,
    ) as client:
        rg = await client.resource_groups.get(
            resource_group_name=resourceGroupName,
        )
        await client.close()
    return rg.serialize(keep_readonly=True)


@resourceGroup.tool(
    name="List-Azure-resource-in-resourceGroup",
    description="List Azure resource in resource group"
    "SubscriptionId, resourceGroupName are required parameters. "
    "It returns the azure resource profile in JSON format. "
    "The profile spec can be found here: https://learn.microsoft.com/en-us/rest/api/resources/resources/list",
)
async def get_azure_resource_group(
    ctx: Context,
    subscriptionId: str = Field(description="The Azure subscription ID."),
    resourceGroupName: str = Field(description="The Azure resource group name."),
) -> list[bytes]:
    """
    Azure resource group profile.
    Args:
            subscriptionId (str): The Azure subscription ID.
            resourceGroupName (str): The Azure resource group name.
    Returns:
            str: The resource list in JSON format.
    """
    resources = []
    async with ResourceManagementClient(
        credential=ctx.request_context.lifespan_context.credential,
        subscription_id=subscriptionId,
        user_agent=USER_AGENT,
    ) as client:
        async for i in client.resources.list_by_resource_group(
            resource_group_name=resourceGroupName,
        ):
            resources.append(i.serialize(keep_readonly=True)) 
        await client.close()
    return resources
