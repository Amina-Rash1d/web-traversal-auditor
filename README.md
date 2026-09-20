# Web Directory & Path Traversal Exposure Assessment

A lightweight, Python-orchestrated security assessment tool. It runs directory enumeration and controlled path traversal testing against a target, correlates the results, and produces a single evidence-backed PDF report — all from one command.

No custom scanner, no reinvented wheels. It automates Gobuster for enumeration, runs a small set of controlled traversal payloads, and turns the raw output into something you can actually read.

## What it does

- Enumerates exposed paths using Gobuster
- Runs controlled path traversal tests against a target parameter
- Classifies results by response content, not just status code
- Preserves raw evidence for every test
- Generates a structured PDF report
- Runs the entire workflow from a single command

## Getting started

```bash
git clone https://github.com/Amina-Rash1d/web-traversal-auditor.git
cd web-traversal-auditor

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Gobuster must be installed and available on your `PATH`.

## Usage

```bash
python3 main.py --url http://127.0.0.1:5003
```

The assessment report is saved to `reports/`, with raw supporting evidence in `evidence/`.

## Built with

Python · Gobuster · Requests · ReportLab · Docker

---
