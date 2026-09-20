from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)


def generate_report(target_url, run_id, enumeration_results, traversal_results):
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    output_file = reports_dir / f"{run_id}_assessment.pdf"

    document = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
    )

    styles = getSampleStyleSheet()

    # -----------------------------
    # Color palette
    # -----------------------------

    NAVY = colors.HexColor("#172033")
    BLUE = colors.HexColor("#2563EB")
    LIGHT_BLUE = colors.HexColor("#EFF6FF")
    GREEN = colors.HexColor("#15803D")
    LIGHT_GREEN = colors.HexColor("#F0FDF4")
    RED = colors.HexColor("#B91C1C")
    LIGHT_RED = colors.HexColor("#FEF2F2")
    AMBER = colors.HexColor("#B45309")
    LIGHT_AMBER = colors.HexColor("#FFFBEB")
    GREY = colors.HexColor("#64748B")
    LIGHT_GREY = colors.HexColor("#F1F5F9")
    BORDER = colors.HexColor("#CBD5E1")
    DARK = colors.HexColor("#1E293B")

    # -----------------------------
    # Styles
    # -----------------------------

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.white,
        alignment=TA_LEFT,
        spaceAfter=0,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#D8E2F0"),
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=NAVY,
        spaceBefore=4,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=14,
        textColor=DARK,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=GREY,
    )

    finding_style = ParagraphStyle(
        "Finding",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=RED,
    )

    code_style = ParagraphStyle(
        "Code",
        parent=styles["BodyText"],
        fontName="Courier",
        fontSize=8.5,
        leading=12,
        textColor=DARK,
    )

    center_small = ParagraphStyle(
        "CenterSmall",
        parent=small_style,
        alignment=TA_CENTER,
    )

    story = []

    # -----------------------------
    # Header
    # -----------------------------

    header = Table(
        [
            [
                Paragraph(
                    "WEB DIRECTORY &amp; PATH TRAVERSAL<br/>"
                    "EXPOSURE ASSESSMENT",
                    title_style,
                )
            ],
            [
                Paragraph(
                    f"Target: {target_url} &nbsp;&nbsp; "
                    f"Assessment ID: {run_id}",
                    subtitle_style,
                )
            ],
        ],
        colWidths=[174 * mm],
    )

    header.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#202B42")),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("TOPPADDING", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 1), (-1, 1), 7),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 9),
            ]
        )
    )

    story.append(header)
    story.append(Spacer(1, 14))

    # -----------------------------
    # Calculate results
    # -----------------------------

    finding_results = [
        test
        for test in traversal_results
        if test["classification"] == "FINDING"
    ]

    blocked_results = [
        test
        for test in traversal_results
        if test["classification"] == "BLOCKED"
    ]

    passed_results = [
        test
        for test in traversal_results
        if test["classification"] == "PASS"
    ]

    # -----------------------------
    # Summary cards
    # -----------------------------

    enumeration_count = len(enumeration_results)
    traversal_count = len(finding_results)

    summary_data = [
        [
            Paragraph("<b>ENUMERATION</b>", center_small),
            Paragraph("<b>TRAVERSAL</b>", center_small),
            Paragraph("<b>CONFIRMED EXPOSURE</b>", center_small),
        ],
        [
            Paragraph(
                f"<font size='18'><b>{enumeration_count}</b></font><br/>"
                f"<font color='#64748B'>findings</font>",
                center_small,
            ),
            Paragraph(
                f"<font size='18'><b>{traversal_count}</b></font><br/>"
                f"<font color='#64748B'>finding</font>",
                center_small,
            ),
            Paragraph(
                "<font size='14'><b>YES</b></font><br/>"
                "<font color='#64748B'>based on observed content</font>",
                center_small,
            ),
        ],
    ]

    summary = Table(
        summary_data,
        colWidths=[58 * mm, 58 * mm, 58 * mm],
        rowHeights=[9 * mm, 18 * mm],
    )

    summary.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT_GREY),
                ("BACKGROUND", (0, 1), (0, 1), LIGHT_BLUE),
                ("BACKGROUND", (1, 1), (1, 1), LIGHT_RED),
                ("BACKGROUND", (2, 1), (2, 1), LIGHT_RED),
                ("TEXTCOLOR", (1, 1), (2, 1), RED),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(summary)
    story.append(Spacer(1, 16))

    # -----------------------------
    # Assessment flow
    # -----------------------------

    story.append(
        Paragraph("ASSESSMENT OVERVIEW", section_style)
    )

    flow = Table(
        [
            [
                Paragraph("<b>Enumeration</b><br/>"
                          "<font color='#64748B'>0 findings</font>",
                          center_small),
                Paragraph("<b>→</b>", center_small),
                Paragraph("<b>Traversal Tests</b><br/>"
                          "<font color='#64748B'>4 requests</font>",
                          center_small),
                Paragraph("<b>→</b>", center_small),
                Paragraph("<b>Evidence</b><br/>"
                          "<font color='#64748B'>Preserved</font>",
                          center_small),
            ]
        ],
        colWidths=[43 * mm, 10 * mm, 48 * mm, 10 * mm, 43 * mm],
    )

    flow.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), LIGHT_BLUE),
                ("BACKGROUND", (2, 0), (2, 0), LIGHT_AMBER),
                ("BACKGROUND", (4, 0), (4, 0), LIGHT_GREEN),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )

    story.append(flow)
    story.append(Spacer(1, 16))

    # -----------------------------
    # Test results
    # -----------------------------

    story.append(
        Paragraph("TEST RESULTS", section_style)
    )

    results_data = [
        [
            Paragraph("<b>TEST</b>", small_style),
            Paragraph("<b>PAYLOAD</b>", small_style),
            Paragraph("<b>HTTP</b>", small_style),
            Paragraph("<b>RESULT</b>", small_style),
        ]
    ]

    for test in traversal_results:
        classification = test["classification"]

        if classification == "FINDING":
            result_text = f"<font color='#B91C1C'><b>{classification}</b></font>"
        elif classification == "PASS":
            result_text = f"<font color='#15803D'><b>{classification}</b></font>"
        else:
            result_text = f"<font color='#B45309'><b>{classification}</b></font>"

        results_data.append(
            [
                Paragraph(test["name"].replace("_", " ").title(), small_style),
                Paragraph(test["payload"], code_style),
                Paragraph(str(test["status"]), small_style),
                Paragraph(result_text, small_style),
            ]
        )

    results_table = Table(
        results_data,
        colWidths=[42 * mm, 72 * mm, 20 * mm, 40 * mm],
        repeatRows=1,
    )

    results_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT_GREY),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(results_table)
    story.append(Spacer(1, 16))

    # -----------------------------
    # Confirmed finding
    # -----------------------------

    story.append(
        Paragraph("CONFIRMED FINDING", section_style)
    )

    if finding_results:
        finding = finding_results[0]

        finding_box = Table(
            [
                [
                    Paragraph(
                        "PATH TRAVERSAL EVIDENCE",
                        ParagraphStyle(
                            "FindingLabel",
                            parent=small_style,
                            fontName="Helvetica-Bold",
                            textColor=RED,
                        ),
                    )
                ],
                [
                    Paragraph(
                        finding["payload"],
                        finding_style,
                    )
                ],
                [
                    Paragraph(
                        "The application returned content consistent with "
                        "access to a file outside the intended document "
                        "directory.",
                        body_style,
                    )
                ],
                [
                    Paragraph(
                        f"<b>HTTP status:</b> {finding['status']} &nbsp;&nbsp; "
                        f"<b>Evidence:</b> {finding['evidence_file']}",
                        small_style,
                    )
                ],
            ],
            colWidths=[174 * mm],
        )

        finding_box.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), LIGHT_RED),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#FCA5A5")),
                    ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.HexColor("#FCA5A5")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        story.append(finding_box)

    else:
        story.append(
            Paragraph(
                "No confirmed traversal finding was identified "
                "in the tested cases.",
                body_style,
            )
        )

    story.append(Spacer(1, 16))

    # -----------------------------
    # Evidence
    # -----------------------------

    story.append(
        Paragraph("EVIDENCE PRESERVED", section_style)
    )

    evidence_files = []

    if enumeration_results:
        evidence_files.append(
            f"evidence/{run_id}/gobuster_raw.txt"
        )

    for test in traversal_results:
        evidence_files.append(test["evidence_file"])

    evidence_rows = []

    for index in range(0, len(evidence_files), 2):
        left = evidence_files[index]
        right = evidence_files[index + 1] if index + 1 < len(evidence_files) else ""

        evidence_rows.append(
            [
                Paragraph(f"• {left}", small_style),
                Paragraph(f"• {right}", small_style),
            ]
        )

    evidence_table = Table(
        evidence_rows,
        colWidths=[87 * mm, 87 * mm],
    )

    evidence_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(evidence_table)
    story.append(Spacer(1, 16))

    # -----------------------------
    # Conclusion
    # -----------------------------

    story.append(
        Paragraph("CONCLUSION", section_style)
    )

    if finding_results:
        conclusion = (
            "Path traversal evidence was confirmed for the tested file "
            "parameter based on observed response content. The supporting "
            "HTTP responses have been preserved as raw evidence."
        )
    else:
        conclusion = (
            "No confirmed path traversal evidence was identified in the "
            "controlled test cases. Raw responses have been preserved "
            "for verification."
        )

    conclusion_box = Table(
        [
            [
                Paragraph(conclusion, body_style)
            ]
        ],
        colWidths=[174 * mm],
    )

    conclusion_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#93C5FD")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )

    story.append(conclusion_box)

    document.build(story)

    print(f"[+] PDF report generated: {output_file}")

    return str(output_file)
