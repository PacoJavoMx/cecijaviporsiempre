import mysql.connector
import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

# === CONFIGURACIÓN ===
DB_CONFIG = {
    "host": "156.67.64.3",         # Cambia por tu host
    "user": "u332392237_weddin",           # Tu usuario MySQL
    "password": "Temporal2025**",    # Tu contraseña MySQL
    "database": "u332392237_cecijaviaccess"      # Tu base de datos
}

TEMPLATE_PATH = "C:/Users/franc/OneDrive/Documents/Invitaciones/Ceci Y Javi/cecijaviporsiempre/cecijavi.png"         # Ruta al archivo PNG de la invitación
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Fuente
OUTPUT_DIR = "C:/Users/franc/OneDrive/Documents/Invitaciones/Ceci Y Javi/cecijaviporsiempre/boletos"       # Carpeta donde guardar los PDFs
URL_BASE = "https://ceciyjaviporsiempre.com/index.html/resumen5.html"  # Enlace base para el QR
QR_POS = (565, 1220)                   # Coordenadas del QR (X, Y)
QR_SIZE = (300, 300)                   # Tamaño del QR
TEXT_OFFSET_Y = 10                     # Espacio entre QR y texto

# === CONECTAR A MYSQL Y LEER DATOS ===
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT codigo_qr, Nombre FROM invitados")  # Ajusta a tu tabla

rows = cursor.fetchall()
cursor.close()
conn.close()

# === CREAR DIRECTORIO DE SALIDA ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === FUNCIÓN PRINCIPAL ===
def generar_pdf(codigo_qr, nombre, template_path, output_path):
    # Crear QR
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(URL_BASE + codigo_qr)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_img.putdata([(255, 255, 255, 0) if px[:3] == (255, 255, 255) else px for px in qr_img.getdata()])
    qr_img = qr_img.resize(QR_SIZE)

    # Cargar plantilla
    fondo = Image.open(template_path).convert("RGBA")
    fondo.paste(qr_img, QR_POS, qr_img)

    # Dibujar texto debajo del QR
    draw = ImageDraw.Draw(fondo)
    font = ImageFont.truetype(FONT_PATH, 36)
    text_pos = (QR_POS[0], QR_POS[1] + QR_SIZE[1] + TEXT_OFFSET_Y)
    draw.text(text_pos, codigo_qr, font=font, fill=(0, 0, 0))

    # Guardar imagen temporal
    temp_img = f"{codigo_qr}_temp.png"
    fondo.save(temp_img)

    # Crear PDF desde imagen
    c = canvas.Canvas(output_path, pagesize=letter)
    c.drawImage(temp_img, 0, 0, width=612, height=792)
    c.save()

    # Limpiar
    os.remove(temp_img)

# === GENERAR TODOS LOS PDF ===
for row in rows:
    codigo = row["codigo_qr"]
    nombre = row.get("Nombre", "").strip().replace(" ", "_")
    nombre_archivo = f"{codigo}.pdf"
    output_path = os.path.join(OUTPUT_DIR, nombre_archivo)
    generar_pdf(codigo, nombre, TEMPLATE_PATH, output_path)

print(f"PDFs generados en: {OUTPUT_DIR}")

import subprocess
subprocess.run(['explorer', OUTPUT_DIR])
