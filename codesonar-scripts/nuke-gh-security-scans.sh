# 1. Set your details
OWNER="wside-adacore-test"
REPO="c_static_analysis_demo"
TOOL="CodeSonar" # Or the exact tool name from the ghost alerts

# 2. Fetch all analysis IDs for that tool
ANALYSES=$(gh api "repos/$OWNER/$REPO/code-scanning/analyses?tool_name=$TOOL" --jq '.[].id')

# 3. Loop through and vaporize them
for id in $ANALYSES; do
    echo "Deleting analysis $id..."
    gh api -X DELETE "repos/$OWNER/$REPO/code-scanning/analyses/$id?confirm_delete=true"
done

echo "Cleanup complete! Refresh your GitHub UI."
