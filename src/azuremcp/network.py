from context import app_lifespan

from pydantic import Field
from mcp.server.fastmcp import Context, FastMCP
from azure.mgmt.network.aio import NetworkManagementClient

# Constants
USER_AGENT = "azure-network-mcp-server/1.0"

# Initialize FastMCP server
virtualNetwork = FastMCP(
    "Azure VirtualNetwork MCP server",
    "This mcp server will operate on Azure virtual network resources.Put subscriptionid, and resource name and get the azure resource profile. SubscriptionId, resourceGroupName and resource name can be parsed from the azure resource id."
    "The resource id should contain providers/Microsoft.Network/networkProfiles",
    dependencies=["azure-mgmt-network", "azure-identity", "aiohttp"],
    lifespan=app_lifespan,
)


@virtualNetwork.tool(
    name="Get-Azure-VirtualNetwork-Profile",
    description="Get Azure Virtual Network profile in JSON format from azure rest api. It contains all of virtual network configurations."
    "SubscriptionId, resourceGroupName and virtualNetworkName are required parameters. "
    "The subscriptionId is the Azure subscription ID, resourceGroupName is the Azure resource group name, and virtualNetworkName is the Azure Virtual Network name."
    "The parameters can be parsed from the azure resource id. "
    "The resource id of virtual network is in the format of /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/networkProfiles/{virtualNetworkName}."
    "It returns the azure VirtualNetwork resource profile in JSON format. "
    "The profile spec can be found here: https://learn.microsoft.com/en-us/rest/api/virtualnetwork/network-profiles/get",
)
async def get_azure_virtualnetwork_profile(
    ctx: Context,
    subscriptionId: str = Field(description="The Azure subscription ID."),
    resourceGroupName: str = Field(description="The Azure resource group name."),
    virtualNetworkName: str = Field(description="The Azure Virtual Network name."),
) -> bytes:
    """
    Azure Virtual Network profile.
    Args:
            subscriptionId (str): The Azure subscription ID.
            resourceGroupName (str): The Azure resource group name.
            virtualNetworkName (str): The Azure Virtual Network name.
    Returns:
            str: The Azure Virtual Network profile in JSON format.
    """
    vnet = None
    async with NetworkManagementClient(
        credential=ctx.request_context.lifespan_context.credential,
        subscription_id=subscriptionId,
        user_agent=USER_AGENT,
    ) as client:
        vnet = await client.virtual_networks.get(
            resource_group_name=resourceGroupName,
            virtual_network_name=virtualNetworkName,
        )
        await client.close()
    return vnet.serialize(keep_readonly=True)

# Initialize FastMCP server
routeTable = FastMCP(
    "Azure RouteTable MCP server",
    "This mcp server will operate on Azure RouteTable resources.Put subscriptionid, and resource name and get the azure resource profile. SubscriptionId, resourceGroupName and resource name can be parsed from the azure resource id."
    "The resource id should contain providers/Microsoft.Network/routeTables",
    dependencies=["azure-mgmt-network", "azure-identity", "aiohttp"],
    lifespan=app_lifespan,
)


@routeTable.tool(
    name="Get-Azure-RouteTable Profile",
    description="Get Azure Route Table profile in JSON format from azure rest api. It contains all of route table configurations."
    "SubscriptionId, resourceGroupName and routeTableName are required parameters. "
    "The subscriptionId is the Azure subscription ID, resourceGroupName is the Azure resource group name, and routeTableName is the Azure Route Table name."
    "The parameters can be parsed from the azure resource id. "
    "The resource id of route table is in the format of /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/routeTables/{routeTableName}."
    "It returns the azure RouteTable resource profile in JSON format. "
    "The profile spec can be found here: https://learn.microsoft.com/en-us/rest/api/virtualnetwork/route-tables/get",
)
async def get_azure_routetable_profile(
    ctx: Context,
    subscriptionId: str = Field(description="The Azure subscription ID."),
    resourceGroupName: str = Field(description="The Azure resource group name."),
    routeTableName: str = Field(description="The Azure Route Table name."),
) -> bytes:
    """
    Azure Route Table profile.
    Args:
            subscriptionId (str): The Azure subscription ID.
            resourceGroupName (str): The Azure resource group name.
            routeTableName (str): The Azure Route Table name.
    Returns:
            str: The Azure Route Table profile in JSON format.
    """
    routeTable = None
    async with NetworkManagementClient(
        credential=ctx.request_context.lifespan_context.credential,
        subscription_id=subscriptionId,
        user_agent=USER_AGENT,
    ) as client:
        routeTable = await client.route_tables.get(
            resource_group_name=resourceGroupName,
            route_table_name=routeTableName,
        )
        await client.close()
    return routeTable.serialize(keep_readonly=True)



# Initialize FastMCP server
securityGroup = FastMCP(
    "Azure network security group MCP server",
    "This mcp server will operate on Azure NetworkSecurityGroup resources.Put subscriptionid, and resource name and get the azure resource profile. SubscriptionId, resourceGroupName and resource name can be parsed from the azure resource id."
    "The resource id should contain providers/Microsoft.Network/networkSecurityGroups",
    dependencies=["azure-mgmt-network", "azure-identity", "aiohttp"],
    lifespan=app_lifespan,
)


@securityGroup.tool(
    name="Get-Azure-NetworkSecurityGroups-Profile",
    description="Get Azure NetworkSecurityGroups profile in JSON format from azure rest api. It contains all of nsg configurations."
    "SubscriptionId, resourceGroupName and routeTableName are required parameters. "
    "The subscriptionId is the Azure subscription ID, resourceGroupName is the Azure resource group name, and NetworkSecurityGroupsName is the Azure NetworkSecurityGroups name."
    "The parameters can be parsed from the azure resource id. "
    "The resource id of nsg is in the format of /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/networkSecurityGroups/{NetworkSecurityGroupsName}."
    "It returns the azure NetworkSecurityGroups resource profile in JSON format. "
    "The profile spec can be found here: https://learn.microsoft.com/en-us/rest/api/virtualnetwork/network-security-groups/get",
)
async def get_azure_networksecuritygroups_profile(
    ctx: Context,
    subscriptionId: str = Field(description="The Azure subscription ID."),
    resourceGroupName: str = Field(description="The Azure resource group name."),
    networkSecurityGroupsName: str = Field(description="The Azure NetworkSecurityGroups name."),
) -> bytes:
    """
    Azure NetworkSecurityGroups profile.
    Args:
            subscriptionId (str): The Azure subscription ID.
            resourceGroupName (str): The Azure resource group name.
            networkSecurityGroupsName (str): The Azure NetworkSecurityGroups name.
    Returns:
            str: The Azure NetworkSecurityGroups profile in JSON format.
    """
    networkSecurityGroup = None
    async with NetworkManagementClient(
        credential=ctx.request_context.lifespan_context.credential,
        subscription_id=subscriptionId,
        user_agent=USER_AGENT,
    ) as client:
        networkSecurityGroup = await client.network_security_groups.get(
            resource_group_name=resourceGroupName,
            network_security_group_name=networkSecurityGroupsName,
        )
        await client.close()
    return networkSecurityGroup.serialize(keep_readonly=True)


# Initialize FastMCP server
natGateway = FastMCP(
    "Azure nat Gateway MCP server",
    "This mcp server will operate on Azure NATGateway resources.Put subscriptionid, and resource name and get the azure resource profile. SubscriptionId, resourceGroupName and resource name can be parsed from the azure resource id."
    "The resource id should contain providers/Microsoft.Network/natGateways",
    dependencies=["azure-mgmt-network", "azure-identity", "aiohttp"],
    lifespan=app_lifespan,
)


@natGateway.tool(
    name="Get-Azure-NATGateway-Profile",
    description="Get Azure NATGateway profile in JSON format from azure rest api. It contains all of nsg configurations."
    "SubscriptionId, resourceGroupName and routeTableName are required parameters. "
    "The subscriptionId is the Azure subscription ID, resourceGroupName is the Azure resource group name, and NATGatewayName is the Azure NATGateway name."
    "The parameters can be parsed from the azure resource id. "
    "The resource id of nsg is in the format of /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/natGateways/{NATGatewayName}."
    "It returns the azure NATGatewayName resource profile in JSON format. "
    "The profile spec can be found here: https://learn.microsoft.com/en-us/rest/api/virtualnetwork/nat-gateways/get",
)
async def get_azure_natGateway_profile(
    ctx: Context,
    subscriptionId: str = Field(description="The Azure subscription ID."),
    resourceGroupName: str = Field(description="The Azure resource group name."),
    NATGatewayName: str = Field(description="The Azure NATGatewayName name."),
) -> bytes:
    """
    Azure NATGateway profile.
    Args:
            subscriptionId (str): The Azure subscription ID.
            resourceGroupName (str): The Azure resource group name.
            NATGatewayName (str): The Azure NATGateway name.
    Returns:
            str: The Azure NATGateway profile in JSON format.
    """
    natGateway = None
    async with NetworkManagementClient(
        credential=ctx.request_context.lifespan_context.credential,
        subscription_id=subscriptionId,
        user_agent=USER_AGENT,
    ) as client:
        natGateway = await client.nat_gateways.get(
            resource_group_name=resourceGroupName,
            nat_gateway_name=NATGatewayName,
        )
        await client.close()
    return natGateway.serialize(keep_readonly=True)

# Initialize FastMCP server
loadBalancer = FastMCP(
    "Azure loadBalancer MCP server",
    "This mcp server will operate on Azure loadBalancer resources.Put subscriptionid, and resource name and get the azure resource profile. SubscriptionId, resourceGroupName and resource name can be parsed from the azure resource id."
    "The resource id should contain providers/Microsoft.Network/loadBalancers",
    dependencies=["azure-mgmt-network", "azure-identity", "aiohttp"],
    lifespan=app_lifespan,
)


@loadBalancer.tool(
    name="Get-Azure-loadBalancer-Profile",
    description="Get Azure loadBalancer profile in JSON format from azure rest api. It contains all of nsg configurations."
    "SubscriptionId, resourceGroupName and routeTableName are required parameters. "
    "The subscriptionId is the Azure subscription ID, resourceGroupName is the Azure resource group name, and loadBalancersName is the Azure loadBalancer name."
    "The parameters can be parsed from the azure resource id. "
    "The resource id of nsg is in the format of /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/loadBalancers/{loadBalancersName}."
    "It returns the azure loadBalancersName resource profile in JSON format. "
    "The profile spec can be found here: https://learn.microsoft.com/en-us/rest/api/load-balancer/load-balancers/get",
)
async def get_azure_loadBalancer_profile(
    ctx: Context,
    subscriptionId: str = Field(description="The Azure subscription ID."),
    resourceGroupName: str = Field(description="The Azure resource group name."),
    loadBalancerName: str = Field(description="The Azure loadBalancer name."),
) -> bytes:
    """
    Azure loadBalancer profile.
    Args:
            subscriptionId (str): The Azure subscription ID.
            resourceGroupName (str): The Azure resource group name.
            loadBalancerName (str): The Azure loadBalancer name.
    Returns:
            str: The Azure loadBalancer profile in JSON format.
    """
    loadBalancer = None
    async with NetworkManagementClient(
        credential=ctx.request_context.lifespan_context.credential,
        subscription_id=subscriptionId,
        user_agent=USER_AGENT,
    ) as client:
        loadBalancer = await client.load_balancers.get(
            resource_group_name=resourceGroupName,
            load_balancer_name=loadBalancerName,
        )
        await client.close()
    return loadBalancer.serialize(keep_readonly=True)

