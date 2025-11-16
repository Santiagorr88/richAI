import openai
import requests
from io import BytesIO
from PIL import Image
import os
prompt_1 = """
Crear una imagen vertical , que transmita una sensación de riqueza y lujo. La imagen debe incluir los siguientes elementos:

1-Un texto prominente que diga 'I'm Rich' en una fuente llamativa y elegante.
2- Elementos visuales que representen riqueza, tales como oro, diamantes, fajos de billetes, joyas o símbolos de lujo y opulencia.
3 - Un logo distintivo que también contenga las palabras 'I'm Rich', diseñado de manera emblemática y sofisticada.
4 - La composición debe ser ideal para un fondo de pantalla vertical, con un equilibrio visual que permita su uso en dispositivos móviles, asegurando que los elementos sean visualmente atractivos y no se sobrecarguen.
5 -La imagen debe evocar un sentido de exclusividad y extravagancia, manteniendo un estilo elegante y moderno."
"""
prompt_2 = """Crear una imagen 1440 x 2560 (QHD)  , que transmita una sensación de riqueza y lujo. La imagen debe 
incluir los siguientes elementos:
1- un texto que dice "Im Rich"
2- debe de hacer referencia a la riqueza
3- un logo de 'Im rich'
4- tiene que ser vertical"""
prompt_3 = """Crear una imagen 1024x1792 , que transmita una sensación de riqueza y lujo. La imagen debe incluir los siguientes elementos:
1- un texto que dice "Im Rich"
2- debe de hacer referencia a la riqueza
3- un logo de 'Im rich'"""
# Coloca aquí tu clave de API de OpenAI
api_key = os.getenv('API_KEY')
# Configurar la clave de API para la autenticación
openai.api_key = api_key

# Crear una solicitud para conectarse al modelo GPT
def generar_imagen(prompt):
    try:
        # Llamada a la API de OpenAI para generar la imagen
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
            model="dall-e-3"
        )

        # Obtener la URL de la imagen generada
        image_url = response['data'][0]['url']

        # Descargar la imagen
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))

        # Mostrar la imagen en el visor de imágenes del sistema
        image.show()

        # Opcional: Guardar la imagen localmente
        image.save("imagen_generada.png")

        print("Imagen generada y guardada exitosamente.")
    except Exception as e:
        print("Ocurrió un error:", e)

# Ejemplo de uso del script
prompt = "Un bosque encantado al atardecer con árboles de colores vibrantes y criaturas mágicas"
generar_imagen(prompt_1)