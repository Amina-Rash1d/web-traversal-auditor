import re
import subprocess
import requests
from pathlib import Path


def run_enumeration(target_url, run_id):
    try:
        response = requests.get(target_url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(f"Target is not reachable: {error}")

    print(f"[+] Target reachable: {target_url}")

    evidence_dir = Path("evidence") / run_id
    evidence_dir.mkdir(parents=True, exist_ok=True)

    output_file = evidence_dir / "gobuster_raw.txt"

    command = [
        "gobuster",
        "dir",
        "-u", target_url,
        "-w", "data/common_paths.txt",
        "-o", str(output_file)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Gobuster failed with exit code {result.returncode}: "
            f"{result.stderr.strip()}"
        )

    if result.stdout.strip():
        output_file.write_text(result.stdout)

    print("[+] Gobuster enumeration completed")
    print(f"[+] Raw output saved to: {output_file}")

    findings = []
    pattern = re.compile(
        r"^/(\S+)\s+\(Status:\s*(\d+)\)\s+\[Size:\s*(\d+)\]"
    )

    for line in output_file.read_text().splitlines():
        match = pattern.search(line)

        if match:
            findings.append({
                "path": f"/{match.group(1)}",
                "status": int(match.group(2)),
                "size": int(match.group(3))
            })

    print(f"[+] Parsed findings: {len(findings)}")

    return findings
