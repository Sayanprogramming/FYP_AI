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
    # Replace special unicode punctuation with ASCII equivalents
    text = text.replace("—", "-").replace("–", "-").replace("’", "'").replace("‘", "'").replace('“', '"').replace('”', '"')
    
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

PRIMARY      = (26,  54,  93)   # deep slate navy
ACCENT       = (229, 62,  62)   # clinical crimson/red
LIGHT_BG     = (247, 250, 252)  # off-white / light slate tint
WHITE        = (255, 255, 255)
DARK_TEXT    = (45,  55,  72)   # charcoal gray for high readability
MID_GREY     = (113, 128, 150)  # cool grey for subtitles/secondary text
BORDER_COLOR = (226, 232, 240)  # border grey


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
        # Top primary color accent band (full width)
        self.set_fill_color(*PRIMARY)
        self.rect(0, 0, 210, 4, "F")

        # Clinic Branding / Logo (Left)
        self.set_text_color(*PRIMARY)
        self.set_font("Arial", "B", 18)
        self.set_xy(15, 10)
        self.cell(100, 8, "HealthForge AI", ln=0)

        # Tagline / Decscription
        self.set_text_color(*MID_GREY)
        self.set_font("Arial", "I", 8.5)
        self.set_xy(15, 18)
        self.cell(100, 5, "Clinical Intelligence & Decision Support", ln=0)

        # Disease assessment badge / metadata (Right)
        self.set_font("Arial", "B", 9.5)
        self.set_xy(135, 10)
        self.set_text_color(*PRIMARY)
        self.cell(60, 7, f"{self._disease.upper()}", border="B", ln=0, align="R")

        # Assessment Date
        self.set_font("Arial", "", 8.5)
        self.set_text_color(*MID_GREY)
        self.set_xy(135, 18)
        today = datetime.today().strftime("%d %b %Y")
        self.cell(60, 5, f"Date: {today}", ln=0, align="R")

        # Divider line separating header from patient info
        self.set_draw_color(*BORDER_COLOR)
        self.set_line_width(0.4)
        self.line(15, 27, 195, 27)

        # Reset text color and explicitly set Y cursor for body content
        self.set_text_color(*DARK_TEXT)
        self.set_y(38)

    # ── Footer ─────────────────────────────────────────────────────────────────
    def footer(self):
        self.set_y(-18)
        self.set_draw_color(*BORDER_COLOR)
        self.set_line_width(0.3)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(2)
        
        # Clinical disclaimer
        self.set_font("Arial", "I", 7.5)
        self.set_text_color(*MID_GREY)
        disclaimer = "DISCLAIMER: This is an AI-generated clinical decision support summary from HealthForge AI — NOT a substitute for professional medical diagnosis, advice, or treatment. Always consult a qualified physician."
        self.set_x(15)
        self.multi_cell(180, 4, _safe(disclaimer), align="C")
        self.set_text_color(*DARK_TEXT)

    # ── Helpers ────────────────────────────────────────────────────────────────
    def section_title(self, title: str):
        """Styled section heading with left accent bar."""
        self.set_fill_color(*PRIMARY)
        self.rect(15, self.get_y(), 3, 6, "F")
        self.set_xy(20, self.get_y() - 0.5)
        self.set_font("Arial", "B", 11)
        self.set_text_color(*PRIMARY)
        self.cell(0, 7, _safe(title), ln=True)
        self.set_text_color(*DARK_TEXT)
        self.ln(2)

    def info_card(self, rows: list[tuple[str, str]]):
        """Render a shaded info card with key-value rows."""
        card_w = 180
        row_height = 7
        card_h = len(rows) * row_height + 6
        start_y = self.get_y()

        # Background card fill
        self.set_fill_color(*LIGHT_BG)
        self.set_draw_color(*BORDER_COLOR)
        self.set_line_width(0.3)
        self.rect(15, start_y, card_w, card_h, "DF")

        # Accent border on the left
        self.set_fill_color(*PRIMARY)
        self.rect(15, start_y, 1.5, card_h, "F")

        # Write the row key-values
        for i, (key, val) in enumerate(rows):
            row_y = start_y + 3 + i * row_height
            self.set_xy(20, row_y)
            self.set_font("Arial", "B", 9.5)
            self.set_text_color(*PRIMARY)
            self.cell(45, 6, _safe(key))
            self.set_font("Arial", "", 9.5)
            self.set_text_color(*DARK_TEXT)
            self.cell(0, 6, _safe(val), ln=False)

        # Set cursor Y below the card
        self.set_xy(15, start_y + card_h + 4)

    def prediction_badge(self, summary: str, is_high_risk: bool):
        """Coloured prediction result banner."""
        if is_high_risk:
            bg_color = (254, 242, 242)     # light red tint
            accent_color = (220, 38, 38)   # clinical crimson
            label = "CLINICAL RISK ASSESSMENT: HIGH RISK / ABNORMAL FINDINGS"
        else:
            bg_color = (240, 253, 244)     # light green tint
            accent_color = (22, 101, 52)   # professional forest green
            label = "CLINICAL RISK ASSESSMENT: LOW RISK / NORMAL FINDINGS"

        # Safely clean and wrap summary text
        clean_summary = _clean_markdown(summary)
        chars_per_line = 95
        num_lines = max(1, (len(clean_summary) // chars_per_line) + 1)
        
        card_w = 180
        card_h = 12 + (num_lines * 5) + 4
        start_y = self.get_y()

        # Shaded background card
        self.set_fill_color(*bg_color)
        self.set_draw_color(*BORDER_COLOR)
        self.set_line_width(0.3)
        self.rect(15, start_y, card_w, card_h, "DF")

        # Bold left status strip (4mm wide)
        self.set_fill_color(*accent_color)
        self.rect(15, start_y, 4, card_h, "F")

        # 1. Assessment Category Label
        self.set_xy(23, start_y + 3.5)
        self.set_font("Arial", "B", 10.5)
        self.set_text_color(*accent_color)
        self.cell(0, 6, _safe(label), ln=False)

        # 2. Detailed Summary Text
        self.set_xy(23, start_y + 10.5)
        self.set_font("Arial", "", 9)
        self.set_text_color(*DARK_TEXT)
        self.multi_cell(165, 5, _safe(clean_summary))
        
        # Set cursor Y below the card
        self.set_xy(15, start_y + card_h + 4)

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
                self.ln(2)
                self.set_font("Arial", "B", 10)
                self.set_text_color(*PRIMARY)
                self.set_x(15)
                self.multi_cell(180, 6, _safe(stripped))
                self.set_font("Arial", "", 10)
                self.set_text_color(*DARK_TEXT)
            elif stripped.startswith("•"):
                self.set_x(19)
                self.cell(5, 6, chr(149))
                self.multi_cell(175, 6, _safe(stripped[1:].strip()))
            else:
                self.set_x(15)
                self.multi_cell(180, 6, _safe(stripped))


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
    pdf.set_margins(15, 38, 15)  # Set consistent margins
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
    msg["Subject"] = f"Your HealthForge AI Report – {disease.title()}"
    msg["From"]    = sender_email
    msg["To"]      = recipient_email
    msg.set_content(
        f"Hello {patient_name},\n\n"
        f"Please find your HealthForge AI health recommendation report for {disease.title()} "
        "attached as a PDF.\n\n"
        "⚠  This is AI-generated guidance only. Always consult a qualified physician.\n\n"
        "Regards,\nHealthForge AI Team"
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
