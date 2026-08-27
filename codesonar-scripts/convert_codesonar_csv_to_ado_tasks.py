#!/usr/bin/env python3
import argparse
import os
import sys
import pandas as pd

def get_warning_level(score):
    """Return full level string and short level tag based on CodeSonar score pivots."""
    if score <= 21:
        return "green (low)", "low"
    elif score <= 56:
        return "yellow (medium)", "medium"
    else:
        return "red (high)", "high"

def convert_codesonar_to_ado(input_csv, output_csv=None, hub_url="http://localhost:7341"):
    # Determine output filename if not explicitly provided
    if not output_csv:
        base, ext = os.path.splitext(input_csv)
        output_csv = f"{base}_for_ado{ext}"
    
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Error: Input file '{input_csv}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{input_csv}': {e}", file=sys.stderr)
        sys.exit(1)

    # Clean hub URL base
    hub_base = hub_url.rstrip('/')

    titles = []
    descriptions = []

    for _, row in df.iterrows():
        score = int(row['score'])
        cs_id = row['id']
        cs_class = row['class']
        significance = row['significance']
        filename = row['file']
        raw_url = str(row['url'])

        level_str, short_level = get_warning_level(score)

        # Build Title
        title = f"[CS_Score {score:03d} ({short_level}), CS_ID {cs_id}, {significance}] {cs_class}, {filename}"
        titles.append(title)

        # Format Hub URL (replace .txt with .html)
        if raw_url.endswith('.txt'):
            html_url = raw_url[:-4] + '.html'
        else:
            html_url = raw_url
        full_hub_link = f"{hub_base}/{html_url.lstrip('/')}"

        # Using single quotes for href prevents pandas from escaping quotes as "" in CSV,
        # which allows Azure DevOps to parse the HTML string properly.
        desc = (
            f"<div><b>CodeSonar Warning ID:</b> {cs_id}</div>"
            f"<div><b>Warning Type:</b> {cs_class}</div>"
            f"<div><b>CodeSonar Score [0-100]:</b> {score}</div>"
            f"<div><b>CodeSonar Warning Level:</b> {level_str}</div>"
            f"<div><b>CodeSonar Warning Significance:</b> {significance}</div>"
            f"<div><b>File:</b> {filename}</div>"
            f"<div><b>Hub Link:</b> <a href='{full_hub_link}'>{full_hub_link}</a></div>"
        )
        descriptions.append(desc)

    # Construct ADO output DataFrame
    ado_df = pd.DataFrame({
        'Work Item Type': 'Task',
        'Title': titles,
        'Description': descriptions,
        'Tags': 'CodeSonar; imported-from-CSV'
    })

    # Export to CSV
    ado_df.to_csv(output_csv, index=False)
    print(f"Successfully converted {len(ado_df)} items: '{input_csv}' -> '{output_csv}'")

def main():
    parser = argparse.ArgumentParser(
        description="Convert CodeSonar CSV report to Azure DevOps Boards import format."
    )
    parser.add_argument(
        "input_csv",
        help="Path to the input CodeSonar CSV report file"
    )
    parser.add_argument(
        "-o", "--output",
        dest="output_csv",
        default=None,
        help="Path to output converted CSV (default: input file suffixed with '_for_ado')"
    )
    parser.add_argument(
        "--hub",
        dest="hub_url",
        default="http://localhost:7341",
        help="CodeSonar Hub base URL (default: http://localhost:7341)"
    )

    args = parser.parse_args()
    convert_codesonar_to_ado(args.input_csv, args.output_csv, args.hub_url)

if __name__ == "__main__":
    main()