#!/usr/bin/env python3
# Copyright (c) Microsoft. All rights reserved.

"""
Validation script for the Azure service principal demo.

This script validates the logic and structure of the minimal_sample_azure.py
without requiring actual Azure credentials.
"""

import ast
import os
import sys
from pathlib import Path


def validate_demo_script():
    """Validate the minimal_sample_azure.py script."""
    script_path = Path(__file__).parent / "samples/getting_started/minimal_sample_azure.py"
    
    print("🔍 Validating minimal_sample_azure.py...")
    
    # Check file exists
    if not script_path.exists():
        print(f"❌ Error: {script_path} not found")
        return False
    
    # Check Python syntax
    with open(script_path, 'r') as f:
        code = f.read()
        try:
            tree = ast.parse(code)
            print("✅ Python syntax is valid")
        except SyntaxError as e:
            print(f"❌ Syntax error: {e}")
            return False
    
    # Check required imports
    required_imports = [
        'AzureOpenAIChatClient',
        'ClientSecretCredential',
        'AzureCliCredential',
        'DefaultAzureCredential'
    ]
    
    for imp in required_imports:
        if imp not in code:
            print(f"❌ Missing import: {imp}")
            return False
    print("✅ All required imports are present")
    
    # Check for get_azure_credential function
    if 'def get_azure_credential()' not in code:
        print("❌ Missing get_azure_credential function")
        return False
    print("✅ get_azure_credential function is present")
    
    # Check for environment variable handling
    env_vars = ['AZURE_CLIENT_ID', 'AZURE_CLIENT_SECRET', 'AZURE_TENANT_ID']
    for var in env_vars:
        if var not in code:
            print(f"❌ Missing environment variable handling: {var}")
            return False
    print("✅ Environment variable handling is correct")
    
    # Check for async main function
    if 'async def main()' not in code:
        print("❌ Missing async main function")
        return False
    print("✅ async main function is present")
    
    return True


def validate_shell_script():
    """Validate the run_minimal_sample_azure.sh script."""
    script_path = Path(__file__).parent / "run_minimal_sample_azure.sh"
    
    print("\n🔍 Validating run_minimal_sample_azure.sh...")
    
    # Check file exists
    if not script_path.exists():
        print(f"❌ Error: {script_path} not found")
        return False
    
    # Check if executable
    if not os.access(script_path, os.X_OK):
        print("⚠️  Warning: Script is not executable (chmod +x required)")
    else:
        print("✅ Script is executable")
    
    # Check content
    with open(script_path, 'r') as f:
        content = f.read()
        
        # Check for shebang
        if not content.startswith('#!/bin/bash'):
            print("❌ Missing or incorrect shebang")
            return False
        print("✅ Shebang is correct")
        
        # Check for required environment variables
        env_vars = ['AZURE_CLIENT_ID', 'AZURE_CLIENT_SECRET', 'AZURE_TENANT_ID']
        for var in env_vars:
            if var not in content:
                print(f"❌ Missing environment variable check: {var}")
                return False
        print("✅ Environment variable checks are present")
        
        # Check for az login command reference
        if 'az login --service-principal' not in content:
            print("❌ Missing az login command reference")
            return False
        print("✅ az login command reference is present")
    
    return True


def validate_documentation():
    """Validate the documentation files."""
    doc_path = Path(__file__).parent / "samples/getting_started/AZURE_SERVICE_PRINCIPAL_DEMO.md"
    
    print("\n🔍 Validating AZURE_SERVICE_PRINCIPAL_DEMO.md...")
    
    # Check file exists
    if not doc_path.exists():
        print(f"❌ Error: {doc_path} not found")
        return False
    
    with open(doc_path, 'r') as f:
        content = f.read()
        
        # Check for key sections
        required_sections = [
            'Prerequisites',
            'Setup',
            'Running the Demo',
            'Authentication Methods',
            'Troubleshooting'
        ]
        
        for section in required_sections:
            if section not in content:
                print(f"❌ Missing section: {section}")
                return False
        print("✅ All required sections are present")
        
        # Check for code examples
        if '```bash' not in content or '```python' not in content:
            print("❌ Missing code examples")
            return False
        print("✅ Code examples are present")
        
        # Check for environment variables documentation
        env_vars = ['AZURE_CLIENT_ID', 'AZURE_CLIENT_SECRET', 'AZURE_TENANT_ID']
        for var in env_vars:
            if var not in content:
                print(f"❌ Missing environment variable documentation: {var}")
                return False
        print("✅ Environment variables are documented")
    
    return True


def validate_env_example():
    """Validate the .env.example file."""
    env_path = Path(__file__).parent / ".env.example"
    
    print("\n🔍 Validating .env.example...")
    
    # Check file exists
    if not env_path.exists():
        print(f"❌ Error: {env_path} not found")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
        
        # Check for service principal variables
        required_vars = [
            'AZURE_CLIENT_ID',
            'AZURE_CLIENT_SECRET',
            'AZURE_TENANT_ID'
        ]
        
        for var in required_vars:
            if var not in content:
                print(f"❌ Missing variable: {var}")
                return False
        print("✅ All service principal variables are present")
    
    return True


def main():
    """Run all validations."""
    print("=" * 60)
    print("Azure Service Principal Demo Validation")
    print("=" * 60)
    
    all_valid = True
    
    all_valid &= validate_demo_script()
    all_valid &= validate_shell_script()
    all_valid &= validate_documentation()
    all_valid &= validate_env_example()
    
    print("\n" + "=" * 60)
    if all_valid:
        print("✅ All validations passed!")
        print("=" * 60)
        return 0
    else:
        print("❌ Some validations failed")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
