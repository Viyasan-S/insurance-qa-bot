
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "raw" / "mock_life_insurance_policy.pdf"


def create_policy():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="PolicyTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#174A7E"),
        fontSize=20,
        leading=26,
    ))

    story = [
        Paragraph(
            "Global Life Assurance",
            styles["PolicyTitle"],
        ),
        Paragraph(
            "Mock Life Insurance Policy",
            styles["Heading1"],
        ),
        Paragraph(
            "Policy ID: MOCK-GLA-001",
            styles["Normal"],
        ),
        Spacer(1, 12),
        Paragraph("1. Basic Death Benefit", styles["Heading2"]),
        Paragraph(
            "This fictional policy provides a basic death benefit "
            "of 10,000,000 yen to the designated beneficiary if the "
            "insured person dies while the policy is active, subject "
            "to the policy terms and exclusions.",
            styles["BodyText"],
        ),
        Spacer(1, 12),
        Paragraph("2. Accidental Death Benefit", styles["Heading2"]),
        Paragraph(
            "The mock Global Life Secure Plan provides an additional "
            "5,000,000 yen accidental death benefit if the insured "
            "person dies as a direct result of a qualifying accident "
            "while the policy is active. The benefit is subject to "
            "policy conditions, exclusions, and claim approval.",
            styles["BodyText"],
        ),
        Spacer(1, 12),
        Paragraph("3. Waiting Period", styles["Heading2"]),
        Paragraph(
            "A 90-day waiting period applies to death resulting from "
            "illness after the policy start date. Accidental death "
            "benefits are subject to the separate accident coverage "
            "conditions in this fictional policy.",
            styles["BodyText"],
        ),
        PageBreak(),
        Paragraph("4. Exclusions", styles["Heading2"]),
        Paragraph(
            "The accidental death benefit does not apply when an "
            "exclusion specified in the policy applies. Examples in "
            "this fictional document include intentional self-harm "
            "and death resulting from participation in specified "
            "illegal activities. Refer to the complete policy terms "
            "for eligibility.",
            styles["BodyText"],
        ),
        Spacer(1, 12),
        Paragraph("5. Claims Process", styles["Heading2"]),
        Paragraph(
            "The beneficiary must submit a claim form, a death "
            "certificate, proof of identity, and any requested "
            "accident investigation documents. The insurer reviews "
            "the submitted documents before making a decision.",
            styles["BodyText"],
        ),
        Spacer(1, 12),
        Paragraph("6. Important Notice", styles["Heading2"]),
        Paragraph(
            "This document is entirely fictional and exists only "
            "for software development, demonstration, and testing. "
            "It is not a real insurance contract or financial advice.",
            styles["BodyText"],
        ),
    ]

    doc.build(story)
    print(f"Policy PDF created: {OUTPUT}")


if __name__ == "__main__":
    create_policy()
