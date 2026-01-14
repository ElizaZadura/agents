#!/usr/bin/env python
"""Diagnostic script to check .env file and API key configuration"""
import os
from pathlib import Path
from dotenv import load_dotenv

print("=" * 60)
print("ENVIRONMENT VARIABLE DIAGNOSTICS")
print("=" * 60)

# Check project root .env
project_root = Path(__file__).parent.parent.parent.parent.parent
env_path = project_root / '.env'

print(f"\n1. .env File Location:")
print(f"   Project root: {project_root}")
print(f"   .env path: {env_path}")
print(f"   .env exists: {env_path.exists()}")

if env_path.exists():
    print(f"   .env file size: {env_path.stat().st_size} bytes")
    with open(env_path, 'r') as f:
        lines = f.readlines()
        print(f"   .env file has {len(lines)} lines")
        
        # Check for OPENAI_API_KEY
        openai_key_found = False
        for i, line in enumerate(lines, 1):
            if 'OPENAI_API_KEY' in line:
                openai_key_found = True
                # Show first and last few chars (masked)
                key_value = line.split('=', 1)[1].strip() if '=' in line else ''
                if key_value:
                    masked = key_value[:7] + '...' + key_value[-4:] if len(key_value) > 11 else '***'
                    print(f"   Line {i}: OPENAI_API_KEY found")
                    print(f"   Value preview: {masked}")
                    print(f"   Value length: {len(key_value)}")
                    has_quotes = key_value.startswith('"') or key_value.startswith("'")
                    print(f"   Has quotes: {has_quotes}")
                    print(f"   Has leading/trailing whitespace: {key_value != key_value.strip()}")
        
        if not openai_key_found:
            print("   ⚠️  OPENAI_API_KEY not found in .env file!")

# Load .env
print(f"\n2. Loading .env file:")
loaded = load_dotenv(dotenv_path=env_path, override=True)
print(f"   load_dotenv returned: {loaded}")

# Check environment variables
print(f"\n3. Environment Variables:")
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"   ✓ OPENAI_API_KEY is set")
    print(f"   Length: {len(api_key)}")
    print(f"   Starts with: {api_key[:7]}...")
    print(f"   Ends with: ...{api_key[-4:]}")
    print(f"   Has whitespace: {api_key != api_key.strip()}")
    
    # Check for common issues
    issues = []
    if api_key.startswith('"') or api_key.startswith("'"):
        issues.append("Key has quotes (remove them)")
    if api_key != api_key.strip():
        issues.append("Key has leading/trailing whitespace")
    if len(api_key) < 20:
        issues.append("Key seems too short")
    if not api_key.startswith('sk-'):
        issues.append("Key doesn't start with 'sk-' (might be wrong format)")
    
    if issues:
        print(f"   ⚠️  Potential issues:")
        for issue in issues:
            print(f"      - {issue}")
    else:
        print(f"   ✓ Key format looks correct")
else:
    print(f"   ✗ OPENAI_API_KEY is NOT set in environment")

# Check other possible variable names
print(f"\n4. Other API Key Variables:")
other_vars = ['ANTHROPIC_API_KEY', 'GEMINI_API_KEY', 'GOOGLE_API_KEY', 'DEEPSEEK_API_KEY']
for var in other_vars:
    val = os.getenv(var)
    if val:
        print(f"   {var}: Set (length: {len(val)})")
    else:
        print(f"   {var}: Not set")

# Check for multiple .env files
print(f"\n5. Checking for other .env files:")
for path in [Path.cwd() / '.env', Path(__file__).parent / '.env', Path(__file__).parent.parent / '.env']:
    if path.exists() and path != env_path:
        print(f"   Found additional .env at: {path}")

print("\n" + "=" * 60)
print("RECOMMENDATIONS:")
print("=" * 60)
if not api_key:
    print("1. Ensure OPENAI_API_KEY is in the .env file at the project root")
    print("2. Format should be: OPENAI_API_KEY=sk-... (no quotes, no spaces)")
elif api_key.startswith('"') or api_key.startswith("'"):
    print("1. Remove quotes from OPENAI_API_KEY in .env file")
    print("2. Should be: OPENAI_API_KEY=sk-... (not OPENAI_API_KEY=\"sk-...\")")
elif api_key != api_key.strip():
    print("1. Remove leading/trailing whitespace from OPENAI_API_KEY")
elif not api_key.startswith('sk-'):
    print("1. Verify the API key format - should start with 'sk-'")
else:
    print("1. API key format looks correct")
    print("2. If still getting 401 error, verify the key is active at:")
    print("   https://platform.openai.com/account/api-keys")
    print("3. Check if the key has usage limits or restrictions")
    print("4. Try regenerating the key if it's old")

print()
