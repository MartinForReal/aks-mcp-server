from context import app_lifespan

from pydantic import Field
from mcp.server.fastmcp import Context, FastMCP
from azure.mgmt.containerservice.aio import ContainerServiceClient

# Initialize FastMCP server
managedCluster = FastMCP(
    "Azure Kubernetes Service MCP server",
    dependencies=["azure-mgmt-containerservice", "azure-identity", "aiohttp"],
    lifespan=app_lifespan,
)

# Constants
USER_AGENT = "aks-mcp-server/1.0"


@managedCluster.tool(
    name="Get-Azure-ManagedClusterProfile",
    description="Get Azure Kubernetes Service (AKS) managed cluster profile in JSON format from azure rest api. It contains all of aks cluster configurations."
    "SubscriptionId, resourceGroupName and clusterName are required parameters. "
    "The subscriptionId is the Azure subscription ID, resourceGroupName is the Azure resource group name, and clusterName is the Azure kubernetes cluster name."
    "The parameters can be parsed from the aks cluster resource id. "
    "The resource id is in the format of /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerService/managedClusters/{clusterName}."
    "It returns the aks managedcluster resource profile in JSON format. "
    "The profile spec can be found here: https://learn.microsoft.com/en-us/rest/api/aks/managedclusters/get?#managedcluster",
)
async def get_azure_kubernetes_profile(
    ctx: Context,
    subscriptionId: str = Field(description="The Azure subscription ID."),
    resourceGroupName: str = Field(description="The Azure resource group name."),
    clusterName: str = Field(description="The Azure kubernetes cluster name."),
) -> bytes:
    """
    Azure Kubernetes Service (AKS) managed cluster profile.
    Args:
            subscriptionId (str): The Azure subscription ID.
            resourceGroupName (str): The Azure resource group name.
            clusterName (str): The Azure resource name.
    Returns:
            str: The AKS resource profile in JSON format.
    """
    mc = None
    async with ContainerServiceClient(
        credential=ctx.request_context.lifespan_context.credential,
        subscription_id=subscriptionId,
        user_agent=USER_AGENT,
    ) as client:
        mc = await client.managed_clusters.get(
            resource_group_name=resourceGroupName, resource_name=clusterName
        )
        await client.close()
    return mc.serialize(keep_readonly=True)
