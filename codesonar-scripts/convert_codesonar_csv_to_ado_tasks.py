#!/usr/bin/env python3
import argparse
import os
import sys
import pandas as pd

def convert_codesonar_to_ado(input_csv, output_csv=None):
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

    # Initialize DataFrame with the same index length as input data
    ado_df = pd.DataFrame(index=df.index)
    
    # Set Work Item Type explicitly
    ado_df['Work Item Type'] = 'Task'

    # Title format: "filename - type - CS-ID <id>"
    ado_df['Title'] = (
        df['file'].astype(str) + ' - ' + 
        df['class'].astype(str) + ' - CS-ID ' + 
        df['id'].astype(str)
    )

    # HTML Description with full warning details
    ado_df['Description'] = (
        "<b>CodeSonar Warning Details:</b><br/>" +
        "<ul>" +
        "  <li><b>ID:</b> " + df['id'].astype(str) + "</li>" +
        "  <li><b>File:</b> " + df['file'].astype(str) + " (Line " + df['line number'].astype(str) + ")</li>" +
        "  <li><b>Procedure:</b> " + df['procedure'].fillna('N/A').astype(str) + "</li>" +
        "  <li><b>Class:</b> " + df['class'].astype(str) + "</li>" +
        "  <li><b>Significance:</b> " + df['significance'].astype(str) + "</li>" +
        "  <li><b>Score:</b> " + df['score'].astype(str) + "</li>" +
        "</ul>"
    )

    # Tags: CodeSonar; CS-ID-<id>; <Warning Type/Class>
    ado_df['Tags'] = (
        "CodeSonar; CS-ID-" + df['id'].astype(str) + 
        "; " + df['class'].astype(str)
    )

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

    args = parser.parse_args()
    convert_codesonar_to_ado(args.input_csv, args.output_csv)

if __name__ == "__main__":
    main()
