import sys
import json
from pathlib import Path

def map_codesonar_score_to_github_cvss(score: float) -> float:
    """
    Maps CodeSonar score (0-100) to GitHub CVSS (0.0-10.0) keeping exact order.
    - Green [0, 21]    -> GitHub Low (0.0 to 3.9)
    - Yellow (21, 56]  -> GitHub Medium (4.0 to 6.9)
    - Red (56, 100]    -> GitHub High/Critical (7.0 to 10.0)
    """
    s = max(0.0, min(100.0, float(score)))

    if s <= 21.0:
        return (s / 21.0) * 3.9
    elif s <= 56.0:
        return 4.0 + ((s - 21.0) / (56.0 - 21.0)) * (6.9 - 4.0)
    else:
        return 7.0 + ((s - 56.0) / (100.0 - 56.0)) * (10.0 - 7.0)

def get_codesonar_score_color(score: float) -> str:
    """
    Returns the color band for a given CodeSonar score.
    """
    if score <= 21.0:
        return "Green (low)"
    elif score <= 56.0:
        return "Yellow (medium)"
    else:
        return "Red (high)"

if len(sys.argv) < 2:
    print("Usage: python3 fixup_sarif.py <input_sarif_path> [output_sarif_path]")
    sys.exit(1)

input_path = Path(sys.argv[1])

if len(sys.argv) >= 3:
    output_path = Path(sys.argv[2])
else:
    output_path = input_path.with_name(f"{input_path.stem}_for_gh_scan{input_path.suffix}")

with open(input_path, "r") as f:
    data = json.load(f)

for run in data.get("runs", []):
    # Set the SARIF category for category-level UI filtering
    run["automationDetails"] = {
        "id": "codesonar-clean"
    }

    tool = run.get("tool", {})
    if "driver" not in tool:
        tool["driver"] = {}
    driver = tool["driver"]

    # Set tool name to isolate from previous tool history
    driver["name"] = "codesonar-scan"

    rules_dict = {rule["id"]: rule for rule in driver.get("rules", [])}
    
    rule_max_scores = {}
    processed_rules = set()

    for result in run.get("results", []):
        rule_id = result.get("ruleId")
        props = result.get("properties", {})

        # 1. Extract rank/score for severity calculation
        raw_rank = result.get("rank") or props.get("rank")
        score_num = None
        score_str = "N/A"
        score_color = "N/A"
        
        if raw_rank is not None:
            try:
                score_num = round(float(raw_rank))
                score_str = str(score_num)
                score_color = get_codesonar_score_color(score_num)
                
                # Track maximum score for this rule ID (to prevent downgrading shared rules)
                if rule_id not in rule_max_scores or score_num > rule_max_scores[rule_id]:
                    rule_max_scores[rule_id] = score_num
            except (ValueError, TypeError):
                pass

        # 2. Build Markdown details box (processed once per shared rule)
        if rule_id in rules_dict and rule_id not in processed_rules:
            rule = rules_dict[rule_id]
            
            # Extract Warning ID
            id_obj = props.get("id", {})
            group_id = id_obj.get("groupId")
            instance_id = id_obj.get("instanceId")

            if group_id is not None and instance_id is not None:
                warning_id = f"{group_id}.{instance_id}"
            elif instance_id is not None:
                warning_id = str(instance_id)
            else:
                warning_id = "N/A"
                
            # Extract Level
            level = result.get("level") or props.get("level") or "warning"
            score_level = str(level).capitalize()
            
            if "properties" not in rule:
                rule["properties"] = {}
            rule["properties"]["Score-Level"] = score_level

            # Construct Markdown sidebar header with the requested labels
            hub_url = result.get("hostedViewerUri") or "#"
            existing_md = rule.get("help", {}).get("markdown", "")
            
            cs_header = (
                f"### CodeSonar Warning Details\n"
                f"- **CS_Warning-ID:** `{warning_id}`\n"
                f"- **CS_Score [0-100]:** `{score_str}`\n"
                f"- **CS_Score-Color:** `{score_color}`\n"
                f"- **CS_Score-Level:** `{score_level}`\n"
            )
            
            if hub_url != "#":
                cs_header += f"- [**Open in CodeSonar Hub**]({hub_url})\n\n"
            else:
                cs_header += "\n"
                
            cs_header += "### Standards & References\n"

            rule["help"]["markdown"] = cs_header + existing_md
            processed_rules.add(rule_id)

    # 3. Apply piecewise mapping to max_score to assign GitHub UI Severity
    for rule_id, rule in rules_dict.items():
        if rule_id in rule_max_scores:
            if "properties" not in rule:
                rule["properties"] = {}
                
            max_score = rule_max_scores[rule_id]
            cvss_mapped = map_codesonar_score_to_github_cvss(max_score)
            
            rule["properties"]["security-severity"] = f"{cvss_mapped:.1f}"

with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"Successfully processed: {input_path} -> {output_path}")
