# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os
from random import randint
from typing import Annotated

from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential, ClientSecretCredential, DefaultAzureCredential


def get_weather(
    location: Annotated[str, "The location to get the weather for."],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


def get_azure_credential():
    """Get Azure credential based on environment variables.
    
    Supports multiple authentication methods:
    1. Service Principal (AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID)
    2. Azure CLI (az login)
    3. Default Azure Credential (fallback)
    
    Returns:
        Azure credential object for authentication.
    """
    # Check if service principal credentials are available
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")
    tenant_id = os.getenv("AZURE_TENANT_ID")
    
    if client_id and client_secret and tenant_id:
        print("Using Service Principal authentication (ClientSecretCredential)")
        return ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
    else:
        # Try Azure CLI credential first, then fall back to DefaultAzureCredential
        try:
            print("Using Azure CLI authentication (AzureCliCredential)")
            return AzureCliCredential()
        except Exception:
            print("Using Default Azure authentication (DefaultAzureCredential)")
            return DefaultAzureCredential()


async def main():
    # Get the appropriate Azure credential
    credential = get_azure_credential()
    
    # Create the chat client with Azure OpenAI
    # Requires AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_CHAT_DEPLOYMENT_NAME environment variables
    client = AzureOpenAIChatClient(credential=credential)
    
    # Create an agent with the weather tool
    agent = client.create_agent(
        name="WeatherAgent",
        instructions="You are a helpful weather agent.",
        tools=get_weather
    )
    
    # Run the agent
    result = await agent.run("What's the weather like in Seattle?")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
