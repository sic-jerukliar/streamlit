from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os
import unicodedata
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

def generatePdf(data):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm

    pdf_paths = []
    os.makedirs("dummypdf", exist_ok=True)

    for _, item in data.iterrows():
        try:
            nama = item['Nama']
            kelas = item['Kelas']
            kehadiran = item['Persentase Kehadiran'] * 100
            time = datetime.now() + timedelta(days=1)
            time = time.strftime("%Y %M %d")

            # Safe filename
            safe_nama = clean_text(nama).replace(" ", "_")
            filename = f"dummypdf/Surat_Panggilan_{safe_nama}.pdf"

            # Buat PDF
            c = canvas.Canvas(filename, pagesize=A4)
            width, height = A4

            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(width / 2, height - 2.5 * cm, "Surat Panggilan Orang Tua")

            c.setFont("Helvetica", 11)
            text = c.beginText(3 * cm, height - 4.5 * cm)
            lines = [
                "Yth. Orang Tua/Wali dari:",
                f"Nama  : {nama}",
                f"Kelas   : {kelas}",
                "",
                f"Siswa atas nama tersebut memiliki persentase kehadiran sebesar {kehadiran:.2f}%. Dengan ini kami",
                "sampaikan bahwa berdasarkan catatan kehadiran. Hal ini berada di bawah ambang batas" ,
                "minimum kehadiran yang telah ditentukan, yaitu 70%. Kami mengundang Bapak/Ibu untuk hadir",
                "ke sekolah guna membahas tindak lanjut akademik.",
                "",
                f"Tanggal : {time}",
                "Waktu    : 09.00 - 11.00 WIB",
                "Tempat  : Ruang BK",
                "",
                "Hormat kami,",
                "Akademik"
            ]
            for line in lines:
                text.textLine(line)
            c.drawText(text)
            c.save()

            pdf_paths.append({
                "nama": nama,
                "pdf_path": filename
            })

        except Exception as e:
            print(f"Gagal membuat PDF untuk {item['Nama']}: {e}")

    return pdf_paths

def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").strip()

def sendEmail(pdf_info_list):
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_SMTP = os.getenv("EMAIL_SMTP", "smtp.gmail.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))

    results = []

    for item in pdf_info_list:
        try:
            nama_asli = item.get("nama", "")
            nama_bersih = clean_text(nama_asli)

            email_tujuan = item.get("email")
            if not email_tujuan:
                # print(f"[WARNING] Email untuk {nama_bersih} kosong, dikirim ke fallback: acinatra@gmail.com")
                email_tujuan = "acinatra@gmail.com"
            else:
                email_tujuan = clean_text(email_tujuan)

            msg = MIMEMultipart()
            msg["From"] = EMAIL_SENDER
            msg["To"] = email_tujuan
            msg["Subject"] = f"Surat Panggilan untuk {nama_bersih}"

            body = f"""
Yth. Orang Tua dari {nama_bersih},

Terlampir kami sampaikan surat panggilan terkait kehadiran siswa.

Hormat kami,
Akademik
"""
            msg.attach(MIMEText(body, "plain", "utf-8"))

            pdf_path = item["pdf_path"]
            with open(pdf_path, "rb") as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(pdf_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
                msg.attach(part)

            with smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)

            # print(f"[INFO] Email terkirim ke {nama_bersih} ({email_tujuan})")
            results.append({"nama": nama_bersih, "status": "Terkirim"})

        except Exception as e:
            # print(f"[ERROR] Gagal kirim email ke {nama_bersih}: {e}")
            results.append({"nama": nama_bersih, "status": f"Gagal - {e}"})

    return results


def generatePdfAndSendEmail(data):
    pdf_info_list = generatePdf(data)
    hasil_kirim = sendEmail(pdf_info_list)
    return hasil_kirim
