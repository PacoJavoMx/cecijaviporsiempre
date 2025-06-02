
import mysql.connector
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import zipfile
from tqdm import tqdm

# === CONFIGURACIÓN ===
DB_CONFIG = {
    "host": "156.67.64.3",
    "user": "u332392237_wedding",
    "password": "Temporal2025**",
    "database": "u332392237_cecijaviaccess"
}

TEMPLATE_PATH = "cecijavi.jpg"
FONT_PATH = "C:/Windows/Fonts/arial.ttf"
OUTPUT_DIR = "boletos"
QR_POS = (450, 500)
QR_SIZE = (600, 650)
TEXT_OFFSET_Y = 10

# === CONECTAR A MYSQL Y LEER DATOS ===
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT codigo_qr, nombre, mesa FROM boletos")
rows = cursor.fetchall()
cursor.close()
conn.close()

# === CREAR DIRECTORIO DE SALIDA ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Vaciar carpeta de salida antes de comenzar
for file in os.listdir(OUTPUT_DIR):
    file_path = os.path.join(OUTPUT_DIR, file)
    if os.path.isfile(file_path):
        os.remove(file_path)

def generar_jpg(codigo_qr, nombre, mesa, template_path, output_path):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(codigo_qr)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#B08C3E", back_color="white").convert("RGBA")
    qr_img.putdata([(255, 255, 255, 0) if px[:3] == (255, 255, 255) else px for px in qr_img.getdata()])
    qr_img = qr_img.resize(QR_SIZE)

    fondo = Image.open(template_path).convert("RGBA")
    fondo.paste(qr_img, QR_POS, qr_img)

    draw = ImageDraw.Draw(fondo)
    font = ImageFont.truetype(FONT_PATH, 69)
    text_y = QR_POS[1] + QR_SIZE[1] + TEXT_OFFSET_Y
    qr_width = QR_SIZE[0]

    # Código QR
    bbox_codigo = draw.textbbox((0, 0), codigo_qr, font=font)
    text_width_codigo = bbox_codigo[2] - bbox_codigo[0]
    text_x_codigo = QR_POS[0] + (qr_width - text_width_codigo) // 2 - 30
    draw.text((text_x_codigo + 30, text_y - 40), codigo_qr, font=font, fill=(176, 140, 62))

    # Nombre
    nombre_limpio = nombre.strip().title()
    bbox_nombre = draw.textbbox((0, 0), nombre_limpio, font=font)
    text_width_nombre = bbox_nombre[2] - bbox_nombre[0]
    text_x_nombre = QR_POS[0] + (qr_width - text_width_nombre) // 2 - 30
    draw.text((text_x_nombre + 20, text_y + 40), nombre_limpio, font=font, fill=(176, 140, 62))

    # Mesa
    mesa_texto = f"Mesa: {mesa}"
    bbox_mesa = draw.textbbox((0, 0), mesa_texto, font=font)
    text_width_mesa = bbox_mesa[2] - bbox_mesa[0]
    text_x_mesa = QR_POS[0] + (qr_width - text_width_mesa) // 2 - 30
    draw.text((text_x_mesa + 20, text_y + 120), mesa_texto, font=font, fill=(176, 140, 62))

    fondo.convert("RGB").save(output_path, "JPEG", quality=95)

# === GENERAR LAS IMÁGENES JPG ===
for row in tqdm(rows, desc="Generando boletos", unit="boleto"):
    codigo = row["codigo_qr"]
    nombre_original = row.get("nombre", "")
    nombre_limpio = nombre_original.strip().title().replace(" ", "_")
    mesa = str(row.get("mesa", "sin_mesa")).replace(" ", "_")

    # Crear subcarpeta por mesa
    mesa_dir = os.path.join(OUTPUT_DIR, mesa)
    os.makedirs(mesa_dir, exist_ok=True)

    nombre_archivo = f"{codigo}_{nombre_limpio}.jpg"
    output_path = os.path.join(mesa_dir, nombre_archivo)
    generar_jpg(codigo, nombre_original, mesa, TEMPLATE_PATH, output_path)

# === CREAR ARCHIVO ZIP ===
ZIP_PATH = os.path.join(OUTPUT_DIR, "invitaciones_cecijavi.zip")
with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file.endswith(".jpg"):
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, OUTPUT_DIR)
                zipf.write(full_path, arcname)

print(f"ZIP generado en: {ZIP_PATH}")
