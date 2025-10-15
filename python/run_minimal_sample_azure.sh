#!/bin/bash

# Script to run the minimal Azure sample with service principal authentication
# 
# This script demonstrates how to use Azure service principal authentication
# to run the Agent Framework Python demo.
#
# Prerequisites:
# 1. Set the following environment variables:
#    - AZURE_CLIENT_ID: Your Azure service principal client ID
#    - AZURE_CLIENT_SECRET: Your Azure service principal client secret
#    - AZURE_TENANT_ID: Your Azure tenant ID
#    - AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint
#    - AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: Your Azure OpenAI deployment name
#
# 2. Ensure you have the Azure CLI installed
#
# Usage:
#   ./run_minimal_sample_azure.sh

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Azure Service Principal Authentication Demo ===${NC}\n"

# Check if required environment variables are set
required_vars=("AZURE_CLIENT_ID" "AZURE_CLIENT_SECRET" "AZURE_TENANT_ID" "AZURE_OPENAI_ENDPOINT" "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo -e "${RED}Error: The following required environment variables are not set:${NC}"
    for var in "${missing_vars[@]}"; do
        echo -e "${RED}  - $var${NC}"
    done
    echo -e "\n${YELLOW}Please set these variables before running this script.${NC}"
    echo -e "${YELLOW}Example:${NC}"
    echo -e "  export AZURE_CLIENT_ID='your-client-id'"
    echo -e "  export AZURE_CLIENT_SECRET='your-client-secret'"
    echo -e "  export AZURE_TENANT_ID='your-tenant-id'"
    echo -e "  export AZURE_OPENAI_ENDPOINT='your-endpoint'"
    echo -e "  export AZURE_OPENAI_CHAT_DEPLOYMENT_NAME='your-deployment-name'"
    exit 1
fi

# Method 1: Use service principal credentials directly (recommended for automation)
echo -e "${GREEN}Method 1: Using service principal credentials from environment variables${NC}"
echo -e "Environment variables detected:"
echo -e "  AZURE_CLIENT_ID: ${AZURE_CLIENT_ID:0:8}..."
echo -e "  AZURE_TENANT_ID: ${AZURE_TENANT_ID:0:8}..."
echo -e "  AZURE_OPENAI_ENDPOINT: ${AZURE_OPENAI_ENDPOINT}"
echo -e "  AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: ${AZURE_OPENAI_CHAT_DEPLOYMENT_NAME}\n"

echo -e "${BLUE}Running the minimal Azure sample...${NC}\n"
python samples/getting_started/minimal_sample_azure.py

echo -e "\n${GREEN}Demo completed successfully!${NC}\n"

# Method 2: Using az login with service principal (alternative approach)
echo -e "${YELLOW}=== Alternative Method: Using 'az login' with service principal ===${NC}"
echo -e "If you prefer to use az login, you can run:"
echo -e "  ${BLUE}az login --service-principal -u \$AZURE_CLIENT_ID -p \$AZURE_CLIENT_SECRET --tenant \$AZURE_TENANT_ID${NC}"
echo -e "  ${BLUE}python samples/getting_started/minimal_sample_azure.py${NC}"
echo -e "\nNote: The script above (minimal_sample_azure.py) will automatically detect and use"
echo -e "either service principal credentials or Azure CLI authentication.\n"
