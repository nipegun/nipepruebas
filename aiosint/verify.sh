#!/bin/bash

# verify-native.sh
# Checks if the native OSINT framework services are running and responding.

cColorRojo='\033[1;31m'
cColorVerde='\033[1;32m'
cFinColor='\033[0m'

echo -e "${cColorVerde}[+] Verifying OSINT Framework Native Installation...${cFinColor}"

# 1. Check if n8n is running (listening on 5678)
if nc -z localhost 5678; then
    echo -e "${cColorVerde}[OK] n8n is listening on port 5678.${cFinColor}"
else
    echo -e "${cColorRojo}[FAIL] n8n is NOT listening on port 5678. Is it running?${cFinColor}"
fi

# 2. Check if Social API is running (listening on 8000)
if nc -z localhost 8000; then
    echo -e "${cColorVerde}[OK] Social API is listening on port 8000.${cFinColor}"
else
    echo -e "${cColorRojo}[FAIL] Social API is NOT listening on port 8000. Is it running?${cFinColor}"
fi

# 3. Test Social API endpoints (Mock check)
# We won't run a full scan but we can check if the server replies.
echo -e "${cColorVerde}[+] Testing Social API response...${cFinColor}"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/holehe/test@example.com)

if [ "$RESPONSE" == "200" ] || [ "$RESPONSE" == "500" ]; then
    # 500 is acceptable here as test@example.com might fail holehe check or return error, 
    # but at least the flask server replied. 
    # A connection refused would clearly fail.
    echo -e "${cColorVerde}[OK] Social API responded with HTTP code $RESPONSE.${cFinColor}"
else
    echo -e "${cColorRojo}[FAIL] Social API responded with HTTP code $RESPONSE (Expected 200 or 500).${cFinColor}"
fi

echo -e "${cColorVerde}[+] Verification Steps Completed.${cFinColor}"
