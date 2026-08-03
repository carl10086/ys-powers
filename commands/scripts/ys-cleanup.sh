#!/bin/bash
set -euo pipefail

TARGET_DIR="${1:-./docs/ys-powers}"
DAYS_AGO="${2:-7}"

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Target directory does not exist: $TARGET_DIR"
    exit 1
fi

# Cross-platform date: macOS uses -v, Linux uses -d
if date -v-${DAYS_AGO}d +%Y-%m-%d >/dev/null 2>&1; then
    CUTOFF=$(date -v-${DAYS_AGO}d +%Y-%m-%d)
else
    CUTOFF=$(date -d "${DAYS_AGO} days ago" +%Y-%m-%d)
fi

echo "Cutoff date: $CUTOFF"
echo "Files with date prefix older than $CUTOFF:"

stale_files=()
while IFS= read -r file; do
    filename=$(basename "$file")
    if [[ "$filename" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
        file_date="${BASH_REMATCH[1]}"
        if [[ "$file_date" < "$CUTOFF" ]]; then
            stale_files+=("$file")
            echo "  $file (date: $file_date)"
        fi
    else
        echo "  [skip] $file (no YYYY-MM-DD prefix)"
    fi
done < <(find "$TARGET_DIR" -type f -print)

if [[ ${#stale_files[@]} -eq 0 ]]; then
    echo "Nothing to clean."
    exit 0
fi

read -p "Delete these files? [y/N] " answer
if [[ "$answer" != "y" && "$answer" != "Y" ]]; then
    echo "Cancelled."
    exit 0
fi

for file in "${stale_files[@]}"; do
    rm "$file"
    echo "Deleted: $file"
done

echo "Done. Deleted ${#stale_files[@]} file(s)."
