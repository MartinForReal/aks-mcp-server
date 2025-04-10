from setuptools import setup, find_packages

setup(
    name="azure-mcp-server",
    version="0.1.0",
    description="A MCP server providing tools to fetch profile for Azure resources for usage by LLMs",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.12",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "aiohttp>=3.11.16",
        "azure-identity>=1.21.0",
        "azure-mgmt-containerservice>=34.2.0",
        "httpx>=0.28.1",
        "azure-mgmt-network>=28.1.0",
        "mcp[cli]>=1.6.0",
        "mcpo>=0.0.10",
        "azure-mgmt-resource>=23.3.0",
        "azure-mgmt-resourcegraph>=8.0.0",
    ],
    include_package_data=True,
)
