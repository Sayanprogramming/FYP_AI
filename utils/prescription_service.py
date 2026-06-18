import re
import smtplib
from email.message import EmailMessage
from fpdf import FPDF
import streamlit as st
from datetime import datetime


# ─────────────────────────────────────────────────────────────────────────────
#  Markdown → Plain-text cleaner
# ─────────────────────────────────────────────────────────────────────────────

def _clean_markdown(text: str) -> str:
    """
    Convert a Markdown string to clean plain text suitable for PDF rendering.
    Removes **, *, #, backticks, and other Markdown syntax while keeping
    meaningful punctuation and structure.
    """
    # Remove horizontal rules
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    # Headers → keep text, remove # symbols
    text = re.sub(r"^#{1,6}\s*(.+)$", r"\1", text, flags=re.MULTILINE)
    # Bold+italic ***text***
    text = re.sub(r"\*{3}(.+?)\*{3}", r"\1", text)
    # Bold **text**
    text = re.sub(r"\*{2}(.+?)\*{2}", r"\1", text)
    # Italic *text* or _text_
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    # Inline code `text`
    text = re.sub(r"`(.+?)`", r"\1", text)
    # Bullet points: * item / - item → •  item
    text = re.sub(r"^\s*[\*\-]\s+", "•  ", text, flags=re.MULTILINE)
    # Numbered list spacing normalisation (leave numbers as-is)
    text = re.sub(r"^\s*(\d+)\.\s+", r"\1. ", text, flags=re.MULTILINE)
    # Remove leftover lone asterisks / underscores
    text = re.sub(r"(?<!\S)[*_](?!\S)", "", text)
    # Collapse 3+ blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _safe(text: str) -> str:
    """Encode to latin-1, replacing any unsupported char with '?'.
    This prevents FPDFUnicodeEncodingException for any stray emoji or
    special character that slips through (e.g. from the AI response)."""
    return text.encode("latin-1", errors="replace").decode("latin-1")


# ─────────────────────────────────────────────────────────────────────────────
#  Colour palette
# ─────────────────────────────────────────────────────────────────────────────

PRIMARY   = (22,  82, 178)   # rich blue
ACCENT    = (235, 87,  87)   # soft red
LIGHT_BG  = (237, 244, 255)  # very light blue tint
WHITE     = (255, 255, 255)
DARK_TEXT = (30,  30,  40)
MID_GREY  = (120, 120, 140)


# ─────────────────────────────────────────────────────────────────────────────
#  Custom PDF class
# ─────────────────────────────────────────────────────────────────────────────

class PrescriptionPDF(FPDF):

    def __init__(self, patient_name: str, disease: str):
        super().__init__()
        self._patient_name = patient_name
        self._disease = disease

    # ── Header ────────────────────────────────────────────────────────────────
    def header(self):
        # Full-width banner
        self.set_fill_color(*PRIMARY)
        self.rect(0, 0, 210, 36, "F")

        # Thin accent stripe at bottom of banner
        self.set_fill_color(*ACCENT)
        self.rect(0, 33, 210, 3, "F")

        # App name (left)
        self.set_text_color(*WHITE)
        self.set_font("Arial", "B", 17)
        self.set_xy(12, 8)
        self.cell(120, 9, "AI Health Prescription", ln=0)

        # Disease badge (right)
        self.set_font("Arial", "B", 10)
        self.set_xy(148, 6)
        self.set_fill_color(*ACCENT)
        self.cell(52, 8, f"  {self._disease.upper()}  ", border=0, fill=True, align="C")

        # Date (right, second line)
        self.set_font("Arial", "", 9)
        self.set_xy(148, 16)
        self.set_fill_color(*PRIMARY)
        today = datetime.today().strftime("%d %b %Y")
        self.cell(52, 7, f"Date: {today}", align="C")

        self.set_text_color(*DARK_TEXT)
        self.ln(16)   # space after header

    # ── Footer ─────────────────────────────────────────────────────────────────
    def footer(self):
        self.set_y(-16)
        self.set_draw_color(*PRIMARY)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(1)
        self.set_font("Arial", "I", 7.5)
        self.set_text_color(*MID_GREY)
        self.cell(
            0, 6,
            _safe("DISCLAIMER: This is AI-generated guidance only — NOT a substitute for professional medical diagnosis. "
            "Always consult a qualified doctor."),
            align="C",
        )
        self.set_text_color(*DARK_TEXT)

    # ── Helpers ────────────────────────────────────────────────────────────────
    def section_title(self, title: str):
        """Styled section heading with left accent bar."""
        self.set_fill_color(*PRIMARY)
        self.rect(10, self.get_y(), 3, 7, "F")
        self.set_xy(15, self.get_y())
        self.set_font("Arial", "B", 11)
        self.set_text_color(*PRIMARY)
        self.cell(0, 7, _safe(title), ln=True)
        self.set_text_color(*DARK_TEXT)
        self.ln(1)

    def info_card(self, rows: list[tuple[str, str]]):
        """Render a shaded info card with key-value rows."""
        card_h = len(rows) * 7 + 6
        self.set_fill_color(*LIGHT_BG)
        self.set_draw_color(*PRIMARY)
        self.set_line_width(0.3)
        self.rect(10, self.get_y(), 190, card_h, "DF")

        start_y = self.get_y() + 3
        for i, (key, val) in enumerate(rows):
            self.set_xy(14, start_y + i * 7)
            self.set_font("Arial", "B", 9.5)
            self.set_text_color(*PRIMARY)
            self.cell(42, 6, _safe(key))
            self.set_font("Arial", "", 9.5)
            self.set_text_color(*DARK_TEXT)
            self.cell(0, 6, _safe(val), ln=False)
        self.ln(card_h + 2)

    def prediction_badge(self, summary: str, is_high_risk: bool):
        """Coloured prediction result banner."""
        fill = (255, 235, 235) if is_high_risk else (230, 255, 240)
        border = ACCENT if is_high_risk else (34, 170, 90)
        label = "[!] HIGH RISK" if is_high_risk else "[OK] LOW RISK"

        self.set_fill_color(*fill)
        self.set_draw_color(*border)
        self.set_line_width(0.5)
        self.rect(10, self.get_y(), 190, 22, "DF")

        self.set_xy(14, self.get_y() + 3)
        self.set_font("Arial", "B", 11)
        self.set_text_color(*border)
        self.cell(0, 6, _safe(label), ln=True)

        self.set_x(14)
        self.set_font("Arial", "", 9)
        self.set_text_color(*DARK_TEXT)
        short = summary if len(summary) <= 100 else summary[:97] + "..."
        self.cell(0, 6, _safe(short), ln=True)
        self.ln(4)

    def body_text(self, text: str):
        """Render multi-line plain body text with smart bullet handling."""
        lines = text.split("\n")
        self.set_font("Arial", "", 10)
        self.set_text_color(*DARK_TEXT)

        for line in lines:
            stripped = line.strip()
            if not stripped:
                self.ln(3)
                continue

            # Section-like lines (ALL CAPS or ends with ':') → mini heading
            if (stripped.endswith(":") and len(stripped) < 60) or stripped.isupper():
                self.set_font("Arial", "B", 10)
                self.set_text_color(*PRIMARY)
                self.set_x(10)
                self.multi_cell(190, 6, _safe(stripped))
                self.set_font("Arial", "", 10)
                self.set_text_color(*DARK_TEXT)
            elif stripped.startswith("•"):
                self.set_x(14)
                self.cell(5, 6, "-")
                self.multi_cell(181, 6, _safe(stripped[1:].strip()))
            else:
                self.set_x(10)
                self.multi_cell(190, 6, _safe(stripped))


# ─────────────────────────────────────────────────────────────────────────────
#  Public API
# ─────────────────────────────────────────────────────────────────────────────

def generate_pdf_bytes(
    patient_name: str,
    age: int,
    disease: str,
    prediction_summary: str,
    prescription_text: str,
) -> bytes:
    """
    Build a beautifully styled prescription PDF entirely in memory.
    Returns raw bytes — nothing is written to disk.
    """
    is_high = "high" in prediction_summary.lower()
    clean_text = _clean_markdown(prescription_text)

    pdf = PrescriptionPDF(patient_name=patient_name, disease=disease)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ── Patient info ──────────────────────────────────────────────────────────
    pdf.section_title("Patient Information")
    pdf.info_card([
        ("Patient Name :", patient_name),
        ("Age          :", str(age) + " years"),
        ("Assessed For :", disease.title()),
    ])

    # ── Prediction result ─────────────────────────────────────────────────────
    pdf.section_title("Prediction Result")
    pdf.prediction_badge(prediction_summary, is_high_risk=is_high)

    # ── AI advice ─────────────────────────────────────────────────────────────
    pdf.section_title("AI-Generated Health Advice")
    pdf.ln(2)
    pdf.body_text(clean_text)

    return bytes(pdf.output())


def send_prescription_email(
    recipient_email: str,
    patient_name: str,
    age: int,
    disease: str,
    prediction_summary: str,
    prescription_text: str,
) -> None:
    """
    Generates a PDF in memory and mails it to recipient_email.
    Raises an exception on failure so the caller can show st.error().
    """
    sender_email    = st.secrets["email"]["SENDER_EMAIL"]
    sender_password = st.secrets["email"]["SENDER_APP_PASSWORD"].replace(" ", "")

    pdf_bytes = generate_pdf_bytes(
        patient_name, age, disease, prediction_summary, prescription_text
    )

    msg = EmailMessage()
    msg["Subject"] = f"Your AI Health Prescription – {disease.title()}"
    msg["From"]    = sender_email
    msg["To"]      = recipient_email
    msg.set_content(
        f"Hello {patient_name},\n\n"
        f"Please find your AI-generated health prescription for {disease.title()} "
        "attached as a PDF.\n\n"
        "⚠  This is AI-generated guidance only. Always consult a qualified doctor.\n\n"
        "Regards,\nAI Health Recommendation System"
    )
    msg.add_attachment(
        pdf_bytes,
        maintype="application",
        subtype="pdf",
        filename=f"Prescription_{disease.replace(' ', '_')}.pdf",
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
