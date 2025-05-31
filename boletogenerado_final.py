
import mysql.connector
import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import zipfile
import subprocess

# === CONFIGURACIÓN ===
DB_CONFIG = {
    "host": "156.67.64.3",
    "user": "u332392237_wedding",
    "password": "Temporal2025**",
    "database": "u332392237_cecijaviaccess"
}

TEMPLATE_PATH = "cecijavi.png"
FONT_PATH = "C:/Windows/Fonts/arial.ttf"
OUTPUT_DIR = "boletos"
QR_POS = (438, 527)
QR_SIZE = (996, 1074)
TEXT_OFFSET_Y = 10

# === CONECTAR A MYSQL Y LEER DATOS ===
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT codigo_qr, nombre FROM boletos")
rows = cursor.fetchall()
cursor.close()
conn.close()

# === CREAR DIRECTORIO DE SALIDA ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === FUNCIÓN PARA GENERAR PDF ===
def generar_pdf(codigo_qr, nombre, template_path, output_path):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(codigo_qr)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#B08C3E", back_color="white").convert("RGBA")
    qr_img.putdata([(255, 255, 255, 0) if px[:3] == (255, 255, 255) else px for px in qr_img.getdata()])
    qr_img = qr_img.resize(QR_SIZE)

    fondo = Image.open(template_path).convert("RGBA")
    fondo.paste(qr_img, QR_POS, qr_img)

    draw = ImageDraw.Draw(fondo)
    font = ImageFont.truetype(FONT_PATH, 36)

    text_y = QR_POS[1] + QR_SIZE[1] + TEXT_OFFSET_Y
    qr_width = QR_SIZE[0]

    # Texto 1: Código QR centrado
    bbox_codigo = draw.textbbox((0, 0), codigo_qr, font=font)
    text_width_codigo = bbox_codigo[2] - bbox_codigo[0]
    text_x_codigo = QR_POS[0] + (qr_width - text_width_codigo) // 2
    draw.text((text_x_codigo, text_y), codigo_qr, font=font, fill=(0, 0, 0))

    # Texto 2: Nombre centrado
    nombre_limpio = nombre.strip().title()
    bbox_nombre = draw.textbbox((0, 0), nombre_limpio, font=font)
    text_width_nombre = bbox_nombre[2] - bbox_nombre[0]
    text_x_nombre = QR_POS[0] + (qr_width - text_width_nombre) // 2
    draw.text((text_x_nombre, text_y + 40), nombre_limpio, font=font, fill=(0, 0, 0))

    temp_img = f"{codigo_qr}_temp.png"
    fondo.save(temp_img)

    c = canvas.Canvas(output_path, pagesize=letter)
    c.drawImage(temp_img, 0, 0, width=612, height=792)
    c.save()
    os.remove(temp_img)

# === GENERAR LOS PDFS ===
for row in rows:
    codigo = row["codigo_qr"]
    nombre = row.get("nombre", "").strip().replace(" ", "_")
    nombre_archivo = f"{codigo}.pdf"
    output_path = os.path.join(OUTPUT_DIR, nombre_archivo)
    generar_pdf(codigo, nombre, TEMPLATE_PATH, output_path)

print(f"PDFs generados en: {OUTPUT_DIR}")

# === CREAR ARCHIVO ZIP ===
ZIP_PATH = os.path.join(OUTPUT_DIR, "invitaciones_cecijavi.zip")
with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in os.listdir(OUTPUT_DIR):
        if file.endswith(".pdf"):
            full_path = os.path.join(OUTPUT_DIR, file)
            zipf.write(full_path, file)

print(f"ZIP generado en: {ZIP_PATH}")

# === ABRIR CARPETA DE SALIDA ===
subprocess.run(['explorer', OUTPUT_DIR])
