import streamlit as st
from utils.image_ai_check import check_image_ai_fake
from PIL import Image
import os, uuid
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as PDFImage, Table, TableStyle, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import matplotlib.pyplot as plt
import qrcode

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AstraVeriX – Deepfake Detection",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- THEME ----------------
theme = st.sidebar.toggle("🌙 Dark Mode", value=True)
bg = "#0e1117" if theme else "#f5f7fb"
glass = "rgba(255,255,255,0.08)" if theme else "rgba(255,255,255,0.7)"

st.markdown(f"""
<style>
body {{ background:{bg}; }}
.glass {{
    background:{glass};
    backdrop-filter: blur(18px);
    border-radius:20px;
    padding:30px;
    box-shadow:0 8px 32px rgba(0,0,0,0.25);
}}
.title {{
    text-align:center;
    font-size:42px;
    font-weight:800;
    background: linear-gradient(90deg,#00ff9c,#00c3ff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}}
.conf-bar {{
    width:100%; height:22px; background:#222;
    border-radius:20px; overflow:hidden;
}}
.conf-fill {{
    height:100%;
    background:linear-gradient(90deg,#ff416c,#ff4b2b,#00ff9c);
    animation:grow 1.5s ease-out;
}}
@keyframes grow {{ from {{width:0%;}} }}
.badge-real {{color:white;background-color:green;padding:5px 20px;border-radius:15px;font-weight:bold;font-size:18px;}}
.badge-fake {{color:white;background-color:red;padding:5px 20px;border-radius:15px;font-weight:bold;font-size:18px;}}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="glass">
    <div class="title">🛡️ AstraVeriX</div>
    <p style="text-align:center;color:gray">
        AI vs Real Image Verification • National Security
    </p>
</div>
""", unsafe_allow_html=True)
st.write("")

# ---------------- USER DETAILS ----------------
st.markdown("<div class='glass'>", unsafe_allow_html=True)
user_name = st.text_input("👤 Full Name")
user_email = st.text_input("📧 Gmail ID")
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader("📤 Drag & Drop Image", type=["jpg","jpeg","png"], label_visibility="collapsed")

if uploaded_file:
    if not user_name or not user_email:
        st.warning("⚠️ Please enter Name & Gmail ID first")
        st.stop()

    os.makedirs("data/uploads", exist_ok=True)
    image_path = f"data/uploads/{uploaded_file.name}"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Metadata
    timestamp = datetime.now().strftime("%d %b %Y | %I:%M %p")
    verification_id = str(uuid.uuid4()).split("-")[0].upper()
    share_link = f"https://astraverix.streamlit.app/?vid={verification_id}"

    col1, col2 = st.columns(2)

    # ---------------- IMAGE DISPLAY ----------------
    with col1:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.image(image_path, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- AI RESULT ----------------
    with col2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        with st.spinner("🔍 AI analyzing image..."):
            result, confidence = check_image_ai_fake(image_path)

        badge_html = f"<span class='badge-real'>REAL</span>" if result=="REAL" else f"<span class='badge-fake'>FAKE</span>"

        st.markdown(f"""
        <p style="text-align:center;color:gray">
        <b>Name:</b> {user_name}<br>
        <b>Email:</b> {user_email}<br>
        <b>Time:</b> {timestamp}<br>
        <b>Verification ID:</b> {verification_id}
        </p>

        <h2 style="text-align:center">{badge_html}</h2>

        <p style="text-align:center">Confidence: <b>{confidence}%</b></p>

        <div class="conf-bar">
            <div class="conf-fill" style="width:{confidence}%;"></div>
        </div>
        """ , unsafe_allow_html=True)

        st.markdown(f"🔗 **Shareable Link:**  `{share_link}`")

        # ---------------- PDF REPORT ----------------
        os.makedirs("data/reports", exist_ok=True)
        pdf_path = f"data/reports/{verification_id}.pdf"
        pdf = SimpleDocTemplate(pdf_path, pagesize=A4)

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('title', fontSize=26, alignment=1, textColor=colors.HexColor("#00c3ff"), leading=28)
        subtitle_style = ParagraphStyle('subtitle', fontSize=16, alignment=1, textColor=colors.black)
        normal_style = styles["Normal"]
        italic_style = styles["Italic"]

        # QR code
        qr = qrcode.QRCode(box_size=4, border=1)
        qr.add_data(share_link)
        qr.make(fit=True)
        qr_img_path = f"data/reports/{verification_id}_qr.png"
        qr.make_image(fill_color="black", back_color="white").save(qr_img_path)

        # Confidence graph
        plt.figure(figsize=(4,2))
        plt.bar(["FAKE","REAL"], [100-confidence, confidence], color=["red","green"])
        plt.title("Prediction Confidence")
        plt.ylabel("Confidence (%)")
        plt.tight_layout()
        graph_path = f"data/reports/{verification_id}_graph.png"
        plt.savefig(graph_path)
        plt.close()

        # Logo/Emblem
        logo_path = "static/logo.png"
        if os.path.exists(logo_path):
            logo_img = PDFImage(logo_path, width=80, height=80)
        else:
            logo_img = None

        # PDF Content
        content = []
        # Gradient background using canvas
        class GradientBackground(Flowable):
            def draw(self):
                c = self.canv
                c.saveState()
                c.setFillColorRGB(0.95, 0.97, 1)
                c.rect(0,0,A4[0],A4[1], fill=True, stroke=False)
                c.restoreState()

        content.append(GradientBackground())
        if logo_img:
            content.append(logo_img)
            content.append(Spacer(1,10))

        content.append(Paragraph("🛡️ AstraVeriX Verification Certificate", title_style))
        content.append(Spacer(1, 15))
        content.append(PDFImage(image_path, width=250, height=250))
        content.append(Spacer(1, 15))

        data = [
            ["Name", user_name],
            ["Email", user_email],
            ["Result", result],
            ["Confidence", f"{confidence}%"],
            ["Timestamp", timestamp],
            ["Verification ID", verification_id]
        ]
        table = Table(data, colWidths=[130,300])
        table.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(1,0),colors.HexColor("#00c3ff")),
            ('TEXTCOLOR',(0,0),(1,0),colors.white),
            ('BACKGROUND',(0,1),(-1,-1),colors.HexColor("#f5f5f5")),
            ('TEXTCOLOR',(0,1),(-1,-1),colors.black),
            ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),
            ('FONTSIZE',(0,0),(-1,-1),12),
            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('GRID',(0,0),(-1,-1),1,colors.gray),
            ('BOX',(0,0),(-1,-1),2,colors.HexColor("#00c3ff"))
        ]))
        content.append(table)
        content.append(Spacer(1,10))

        # Graph + QR code
        img_graph = PDFImage(graph_path, width=300, height=150)
        img_qr = PDFImage(qr_img_path, width=120, height=120)
        tbl = Table([[img_graph, img_qr]], colWidths=[320, 120])
        tbl.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'BOTTOM')]))
        content.append(tbl)
        content.append(Spacer(1,15))

        content.append(Paragraph(
            "This certificate is AI-generated using AstraVeriX Deepfake Detection by AlphaAryX (Aryan). It is digitally verifiable and protected.",
            italic_style
        ))

        pdf.build(content)

        # Download button
        with open(pdf_path, "rb") as f:
            st.download_button(
                "📜 Download Premium PDF Certificate",
                data=f,
                file_name=f"AstaVeriX_{verification_id}.pdf"
            )

        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div style="text-align:center;color:gray;padding:20px;font-size:14px;">
© 2025 <b>AstraVeriX</b> | Cyber Security & Deepfake Defense | Made by AlphaAryX (Aryan)
</div>
""", unsafe_allow_html=True)
