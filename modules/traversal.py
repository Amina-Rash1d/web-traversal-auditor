import requests
from pathlib import Path
from html import unescape
import re


def run_traversal_tests(target_url, run_id):
    evidence_dir = Path("evidence") / run_id
    evidence_dir.mkdir(parents=True, exist_ok=True)

    test_cases = [
        {
            "name": "baseline",
            "filename": "hello.txt",
            "expected": "normal_file"
        },
        {
            "name": "confirmed_traversal",
            "filename": "../path-traversal-example-app.py",
            "expected": "traversal"
        },
        {
            "name": "deeper_traversal",
            "filename": "../../path-traversal-example-app.py",
            "expected": "traversal"
        },
        {
            "name": "negative_control",
            "filename": "does-not-exist.txt",
            "expected": "nonexistent"
        }
    ]

    results = []

    for index, test in enumerate(test_cases, start=1):
        response_file = evidence_dir / f"traversal_{index}_response.txt"

        try:
            response = requests.get(
                target_url,
                params={"file": test["filename"]},
                timeout=5
            )
        except requests.RequestException as error:
            raise RuntimeError(
                f"Traversal request failed for {test['name']}: {error}"
            )

        body = response.text
        response_file.write_text(body)

        snippet = " ".join(body.split())[:200]

        classification = classify_response(
            test["expected"],
            test["filename"],
            response.status_code,
            body
        )

        result = {
            "name": test["name"],
            "payload": test["filename"],
            "url": response.url,
            "status": response.status_code,
            "length": len(body),
            "snippet": snippet,
            "classification": classification,
            "evidence_file": str(response_file)
        }

        results.append(result)

        print(
            f"[+] {test['name']}: "
            f"HTTP {response.status_code}, "
            f"{classification}"
        )
        print(f"    Payload: {test['filename']}")
        print(f"    Response length: {len(body)}")
        print(f"    Evidence: {response_file}")

    print(f"[+] Traversal tests completed: {len(results)}")

    return results


def classify_response(expected, filename, status_code, body):
    if expected == "normal_file":
        if status_code == 200 and "Hello!" in body:
            return "PASS"

        return "BLOCKED"

    if expected == "nonexistent":
        if "Document not found in repository" in body:
            return "PASS"

        return "BLOCKED"

    if expected == "traversal":
        decoded_body = unescape(body)

        title_match = re.search(
            r'<h2 class="document-title">(.*?)</h2>',
            decoded_body,
            re.DOTALL
        )

        document_title = ""
        if title_match:
            document_title = title_match.group(1).strip()

        source_markers = [
            "from flask import Flask",
            "app = Flask(__name__)",
            "FILES_DIR = 'files'",
            "@app.route"
        ]

        source_marker_count = sum(
            marker in decoded_body
            for marker in source_markers
        )

        if (
            status_code == 200
            and document_title == filename
            and source_marker_count >= 2
        ):
            return "FINDING"

        return "BLOCKED"

    return "BLOCKED"
