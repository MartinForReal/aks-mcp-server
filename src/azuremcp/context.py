
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from azure.identity.aio import DefaultAzureCredential
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP 

@dataclass
class AppContext:
    credential: DefaultAzureCredential

@asynccontextmanager
async def app_lifespan(_: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    credential = DefaultAzureCredential()
    try:
        yield AppContext(credential=credential)
    finally:
        await credential.close()
