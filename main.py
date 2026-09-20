import argparse
from datetime import datetime
from shutil import which

import requests

from modules.enumeration import run_enumeration
from modules.traversal import run_traversal_tests
from modules.reporting import generate_report


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Web Directory & Path Traversal Exposure Assessment"
    )

    parser.add_argument(
        "--url",
        required=True,
        help="Target URL to assess"
    )

    return parser.parse_args()


def check_dependencies():
    if which("gobuster") is None:
        raise RuntimeError(
            "Gobuster is not installed or not available in PATH."
        )


def check_target(target_url):
    try:
        response = requests.get(target_url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(
            f"Target is not reachable: {error}"
        )


def generate_run_id():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"audit_{timestamp}"


def main():
    args = parse_arguments()

    target_url = args.url.rstrip("/")
    run_id = generate_run_id()

    print("=" * 60)
    print("Web Directory & Path Traversal Exposure Assessment")
    print("=" * 60)
    print(f"Target: {target_url}")
    print(f"Run ID: {run_id}")

    print("\n[1] Checking dependencies...")
    check_dependencies()
    print("[+] Gobuster available")

    print("\n[2] Checking target reachability...")
    check_target(target_url)
    print(f"[+] Target reachable: {target_url}")

    print("\n[3] Running directory enumeration...")
    enumeration_results = run_enumeration(
        target_url,
        run_id
    )

    print("\n[4] Running path traversal tests...")
    traversal_results = run_traversal_tests(
        target_url,
        run_id
    )

    print("\n[5] Generating assessment report...")
    report_file = generate_report(
        target_url,
        run_id,
        enumeration_results,
        traversal_results
    )

    findings = [
        test
        for test in traversal_results
        if test["classification"] == "FINDING"
    ]

    print("\n" + "=" * 60)
    print("Assessment completed")
    print("=" * 60)

    print(f"\nEnumeration findings: {len(enumeration_results)}")
    print(f"Traversal tests: {len(traversal_results)}")
    print(f"Confirmed traversal findings: {len(findings)}")
    print(f"PDF report: {report_file}")


if __name__ == "__main__":
    main()
