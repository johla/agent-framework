# Running the Simple Python Demo with Azure Service Principal Authentication

This guide demonstrates how to run the Agent Framework Python demo using Azure service principal authentication.

## Prerequisites

1. **Azure OpenAI Service**: An Azure OpenAI resource with a deployed chat model
2. **Azure Service Principal**: A service principal with appropriate permissions
3. **Python 3.10+**: Installed on your system
4. **Agent Framework**: Installed via pip or uv

## Setup

### 1. Install Agent Framework

```bash
# Using pip
pip install agent-framework --pre

# Or using uv (recommended for development)
uv pip install agent-framework --pre
```

### 2. Configure Environment Variables

Set the following environment variables for service principal authentication:

```bash
export AZURE_CLIENT_ID="your-service-principal-client-id"
export AZURE_CLIENT_SECRET="your-service-principal-client-secret"
export AZURE_TENANT_ID="your-azure-tenant-id"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="your-deployment-name"
```

Alternatively, create a `.env` file in the `python` directory:

```env
AZURE_CLIENT_ID=your-service-principal-client-id
AZURE_CLIENT_SECRET=your-service-principal-client-secret
AZURE_TENANT_ID=your-azure-tenant-id
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your-deployment-name
```

## Running the Demo

### Method 1: Using Service Principal Credentials (Recommended)

The demo script automatically detects service principal credentials from environment variables:

```bash
cd python
python samples/getting_started/minimal_sample_azure.py
```

Or use the provided shell script:

```bash
cd python
./run_minimal_sample_azure.sh
```

### Method 2: Using Azure CLI with Service Principal

If you prefer to use `az login` with service principal:

```bash
# Login using service principal
az login --service-principal \
  -u $AZURE_CLIENT_ID \
  -p $AZURE_CLIENT_SECRET \
  --tenant $AZURE_TENANT_ID

# Run the demo
cd python
python samples/getting_started/minimal_sample_azure.py
```

The demo script will automatically use Azure CLI credentials when service principal environment variables are not set.

## Authentication Methods Supported

The `minimal_sample_azure.py` script supports multiple authentication methods in the following priority order:

1. **Service Principal (ClientSecretCredential)**: Uses `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, and `AZURE_TENANT_ID` environment variables
2. **Azure CLI (AzureCliCredential)**: Uses credentials from `az login`
3. **Default Azure Credential**: Falls back to default credential chain

## Sample Code

The demo creates a simple weather agent using Azure OpenAI:

```python
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import ClientSecretCredential

# Create credential
credential = ClientSecretCredential(
    tenant_id=os.getenv("AZURE_TENANT_ID"),
    client_id=os.getenv("AZURE_CLIENT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET")
)

# Create chat client
client = AzureOpenAIChatClient(credential=credential)

# Create agent
agent = client.create_agent(
    name="WeatherAgent",
    instructions="You are a helpful weather agent.",
    tools=get_weather
)

# Run agent
result = await agent.run("What's the weather like in Seattle?")
```

## Troubleshooting

### Missing Environment Variables

If you see an error about missing environment variables, ensure all required variables are set:
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `AZURE_TENANT_ID`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`

### Authentication Errors

If authentication fails:
1. Verify your service principal credentials are correct
2. Ensure the service principal has appropriate permissions on the Azure OpenAI resource
3. Check that the tenant ID matches your Azure subscription

Required RBAC roles for Azure OpenAI:
- **Cognitive Services OpenAI User**: For using the API
- **Cognitive Services OpenAI Contributor**: For creating resources

### Azure CLI Login

If using `az login`, verify you're logged in:

```bash
az account show
```

## Additional Resources

- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/cognitive-services/openai/)
- [Azure Service Principal Authentication](https://learn.microsoft.com/azure/developer/python/sdk/authentication-overview)
- [Agent Framework Python Documentation](../README.md)
