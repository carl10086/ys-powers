#!/bin/bash
# Force refresh Cursor usage data from Cursor API

CREDENTIALS="$HOME/.config/tokscale/cursor-credentials.json"
CACHE_DIR="$HOME/.config/tokscale/cursor-cache"
TOKEN=$(cat "$CREDENTIALS" 2>/dev/null | jq -r '.accounts[.activeAccountId].sessionToken')

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
    echo "Error: No Cursor credentials found. Run 'tokscale cursor login' first."
    exit 1
fi

echo "Fetching fresh data from Cursor API..."
curl -s "https://cursor.com/api/dashboard/export-usage-events-csv?strategy=tokens" \
    -H "Cookie: WorkosCursorSessionToken=$TOKEN" \
    -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
    > "$CACHE_DIR/usage.csv.new"

if grep -q "^Date," "$CACHE_DIR/usage.csv.new"; then
    mv "$CACHE_DIR/usage.csv.new" "$CACHE_DIR/usage.csv"
    echo "Success! $(grep -c "^\"" "$CACHE_DIR/usage.csv") rows updated."
    echo "Date range:"
    grep "^\"" "$CACHE_DIR/usage.csv" | cut -d'"' -f2 | sort | head -1
    grep "^\"" "$CACHE_DIR/usage.csv" | cut -d'"' -f2 | sort | tail -1
else
    echo "Error: Failed to fetch data"
    cat "$CACHE_DIR/usage.csv.new"
fi
