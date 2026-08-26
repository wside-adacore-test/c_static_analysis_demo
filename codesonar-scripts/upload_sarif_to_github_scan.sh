#!/usr/bin/env bash
set -eo pipefail

usage() {
  echo "Usage: $0 <path-to-sarif-file> [owner/repo]"
  echo ""
  echo "Examples:"
  echo "  $0 /path/to/codesonar-results.sarif"
  echo "  $0 /path/to/codesonar-results.sarif myuser/myrepo"
  exit 1
}

# 1. Validate argument
if [ -z "$1" ]; then
  echo "[!] Error: Missing SARIF file path argument."
  usage
fi

SARIF_FILE="$1"

# 2. Check if file exists
if [ ! -f "$SARIF_FILE" ]; then
  echo "[!] Error: SARIF file '$SARIF_FILE' does not exist."
  exit 1
fi

echo "[*] Found SARIF file: $SARIF_FILE"

# 3. Resolve repository name
if [ -n "$2" ]; then
  REPO="$2"
else
  echo "[*] Auto-detecting repository with gh CLI..."
  REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)
fi

if [ -z "$REPO" ]; then
  echo "[!] Error: Could not detect GitHub repository."
  echo "    Please pass it explicitly: $0 $SARIF_FILE owner/repo"
  exit 1
fi

echo "[*] Target Repository: $REPO"

# 4. Resolve Git commit and ref
echo "[*] Reading Git metadata..."
COMMIT_SHA=$(git rev-parse HEAD 2>/dev/null || true)
REF=$(git rev-parse --symbolic-full-name HEAD 2>/dev/null || true)

if [ -z "$COMMIT_SHA" ] || [ -z "$REF" ]; then
  echo "[!] Error: Failed to read Git commit/ref."
  echo "    Ensure you are running this command from inside your cloned git directory."
  exit 1
fi

echo "[*] Commit SHA: $COMMIT_SHA"
echo "[*] Branch Ref: $REF"

# 5. Compress SARIF
echo "[*] Compressing SARIF file..."
GZIP_B64=$(gzip -c "$SARIF_FILE" | base64 -w0)

# 6. Upload
echo "[*] Sending API request to GitHub Code Scanning..."
RESPONSE=$(gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/code-scanning/sarifs" \
  -f commit_sha="$COMMIT_SHA" \
  -f ref="$REF" \
  -f sarif="$GZIP_B64" \
  -f tool_name="CodeSonar")

echo "[+] Upload complete!"
echo "$RESPONSE"
