import sys
import json
import argparse
import logging
from .validate import validate_latex

def main():
    """
    Validates LaTeX expressions from a file or standard input, outputting results as JSON.

    Expects one LaTeX expression per line. Outputs a JSON array of validation results.
    """
    parser = argparse.ArgumentParser(
        description="Validate LaTeX expressions from a file or standard input.",
        epilog="Example: echo '\\textbf{test}' | latex-validator"
    )
    parser.add_argument('-f', '--file', type=str, help="Path to a file containing LaTeX expressions.")
    parser.add_argument('-o', '--output', type=str, help="Path to output JSON file (default: stdout).")
    parser.add_argument('--encoding', type=str, default='utf-8', help="File encoding (default: utf-8).")
    parser.add_argument('--verbose', action='store_true', help="Enable verbose output.")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    input_source = None
    if args.file:
        try:
            input_source = open(args.file, 'r', encoding=args.encoding)
        except FileNotFoundError:
            print(json.dumps([{"error": f"File not found: {args.file}"}]), file=sys.stderr)
            sys.exit(1)
        except UnicodeDecodeError:
            print(json.dumps([{"error": f"Invalid encoding in file: {args.file}"}]), file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(json.dumps([{"error": f"Permission denied: {args.file}"}]), file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(json.dumps([{"error": f"Error opening file {args.file}: {str(e)}"}]), file=sys.stderr)
            sys.exit(1)
    else:
        if sys.stdin.isatty():
            print(json.dumps([{"error": "No input provided via stdin"}]), file=sys.stderr)
            sys.exit(1)
        input_source = sys.stdin

    results = []
    with input_source:
        for line in input_source:
            logging.debug(f"Processing line: {line.strip()}")
            validation_result = validate_latex(line)
            results.append(validation_result)

    if not results:
        results = [{"error": "No valid LaTeX expressions processed"}]

    output_json = json.dumps(results, indent=2)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as out_file:
                out_file.write(output_json)
            logging.info(f"Output written to {args.output}")
        except Exception as e:
            print(json.dumps([{"error": f"Error writing to output file {args.output}: {str(e)}"}]), file=sys.stderr)
            sys.exit(1)
    else:
        print(output_json)