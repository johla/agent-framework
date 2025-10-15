# Example Usage and Expected Output

This document demonstrates the expected behavior when running the Azure service principal demo.

## Prerequisites Setup

```bash
# Set environment variables
export AZURE_CLIENT_ID="12345678-1234-1234-1234-123456789abc"
export AZURE_CLIENT_SECRET="your-secret-here"
export AZURE_TENANT_ID="87654321-4321-4321-4321-cba987654321"
export AZURE_OPENAI_ENDPOINT="https://my-openai-resource.openai.azure.com/"
export AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4o-mini"
```

## Running the Demo

### Option 1: Direct Python Execution

```bash
cd python
python samples/getting_started/minimal_sample_azure.py
```

**Expected Output:**
```
Using Service Principal authentication (ClientSecretCredential)
The weather in Seattle is sunny with a high of 22°C.
```

### Option 2: Using the Shell Script

```bash
cd python
./run_minimal_sample_azure.sh
```

**Expected Output:**
```
=== Azure Service Principal Authentication Demo ===

Method 1: Using service principal credentials from environment variables
Environment variables detected:
  AZURE_CLIENT_ID: 12345678...
  AZURE_TENANT_ID: 87654321...
  AZURE_OPENAI_ENDPOINT: https://my-openai-resource.openai.azure.com/
  AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: gpt-4o-mini

Running the minimal Azure sample...

Using Service Principal authentication (ClientSecretCredential)
The weather in Seattle is sunny with a high of 22°C.

Demo completed successfully!

=== Alternative Method: Using 'az login' with service principal ===
If you prefer to use az login, you can run:
  az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
  python samples/getting_started/minimal_sample_azure.py

Note: The script above (minimal_sample_azure.py) will automatically detect and use
either service principal credentials or Azure CLI authentication.
```

### Option 3: Using az login

```bash
# Login with service principal
az login --service-principal \
  -u $AZURE_CLIENT_ID \
  -p $AZURE_CLIENT_SECRET \
  --tenant $AZURE_TENANT_ID

# Run the demo
cd python
python samples/getting_started/minimal_sample_azure.py
```

**Expected Output:**
```
Using Azure CLI authentication (AzureCliCredential)
The weather in Seattle is cloudy with a high of 18°C.
```

## Validation

Run the validation script to verify the implementation:

```bash
cd python
python3 validate_azure_demo.py
```

**Expected Output:**
```
============================================================
Azure Service Principal Demo Validation
============================================================
🔍 Validating minimal_sample_azure.py...
✅ Python syntax is valid
✅ All required imports are present
✅ get_azure_credential function is present
✅ Environment variable handling is correct
✅ async main function is present

🔍 Validating run_minimal_sample_azure.sh...
✅ Script is executable
✅ Shebang is correct
✅ Environment variable checks are present
✅ az login command reference is present

🔍 Validating AZURE_SERVICE_PRINCIPAL_DEMO.md...
✅ All required sections are present
✅ Code examples are present
✅ Environment variables are documented

🔍 Validating .env.example...
✅ All service principal variables are present

============================================================
✅ All validations passed!
============================================================
```

## Error Scenarios

### Missing Environment Variables

If you run the shell script without setting environment variables:

```bash
cd python
./run_minimal_sample_azure.sh
```

**Expected Output:**
```
=== Azure Service Principal Authentication Demo ===

Error: The following required environment variables are not set:
  - AZURE_CLIENT_ID
  - AZURE_CLIENT_SECRET
  - AZURE_TENANT_ID
  - AZURE_OPENAI_ENDPOINT
  - AZURE_OPENAI_CHAT_DEPLOYMENT_NAME

Please set these variables before running this script.
Example:
  export AZURE_CLIENT_ID='your-client-id'
  export AZURE_CLIENT_SECRET='your-client-secret'
  export AZURE_TENANT_ID='your-tenant-id'
  export AZURE_OPENAI_ENDPOINT='your-endpoint'
  export AZURE_OPENAI_CHAT_DEPLOYMENT_NAME='your-deployment-name'
```

## Authentication Flow Demonstration

The demo automatically selects the appropriate authentication method:

1. **When service principal credentials are set:**
   ```
   Using Service Principal authentication (ClientSecretCredential)
   ```

2. **When only Azure CLI is configured (after `az login`):**
   ```
   Using Azure CLI authentication (AzureCliCredential)
   ```

3. **When neither is available:**
   ```
   Using Default Azure authentication (DefaultAzureCredential)
   ```

## Integration with CI/CD

For automated pipelines, use service principal credentials:

```yaml
# Example GitHub Actions workflow
steps:
  - name: Run Azure Demo
    env:
      AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
      AZURE_CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
      AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
      AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
      AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: ${{ secrets.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME }}
    run: |
      cd python
      python samples/getting_started/minimal_sample_azure.py
```

## Notes

- The weather output will vary as it uses **simulated/mock weather data** with random conditions and temperatures (not real weather data)
- This is a demonstration of tool calling capabilities, not an actual weather service
- Authentication method used is automatically selected based on available credentials
- All methods produce the same functional result with the agent
