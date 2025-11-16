import qrcode
from PIL import Image, ImageDraw, ImageFont

# Contenido del QR
qr_content = "https://www.google.com/"

# Generar el código QR
qr = qrcode.QRCode(
    version=1,  # Controla el tamaño del QR (1 es el más pequeño)
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,  # Tamaño de cada caja del QR
    border=2,  # Grosor del borde
)
qr.add_data(qr_content)
qr.make(fit=True)

# Crear la imagen del QR
qr_img = qr.make_image(fill_color="white", back_color='black')

# Cargar la imagen de fondo proporcionada por el usuario
background = Image.open("logo_im_rich.png").convert("RGBA")

# Pegar el código QR en la imagen de fondo
qr_size = 150
qr_img = qr_img.resize((qr_size, qr_size))
qr_position = (10, background.height - qr_size - 10)
qr_img = qr_img.convert("RGBA")
background.paste(qr_img, qr_position, qr_img)

# Añadir texto "I'M Rich" debajo del QR
draw = ImageDraw.Draw(background)
font = ImageFont.load_default()  # Puedes reemplazar esto con una fuente personalizada si tienes una
text = "I'M Rich"
text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
text_position = ((background.width - text_width) // 2, qr_position[1] + qr_size + 10)

# Guardar la imagen completa como tarjeta o wallpaper
background.save("im_rich_wallpaper.png", format="PNG")

# Mostrar la imagen generada
background.show()

print("El código QR ha sido generado, guardado como 'im_rich_wallpaper.png' y se muestra en pantalla.")
