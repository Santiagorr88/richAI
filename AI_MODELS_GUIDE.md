# Guía de Configuración de Modelos AI 🤖

Esta guía te explica cómo configurar y usar diferentes modelos de IA para generar imágenes en **I'm Rich AI**.

## 📋 Modelos Disponibles

### 1. **Google Gemini (Imagen 3.0)**
- **Proveedor**: Google
- **Calidad**: Alta calidad, muy realista
- **Tamaño**: Vertical (1024x1792) perfecto para móvil
- **Costo**: ~$0.04 por imagen
- **Recomendado para**: Imágenes de alta calidad con buen detalle

### 2. **DALL-E 3**
- **Proveedor**: OpenAI
- **Calidad**: Ultra HD, excelente comprensión del prompt
- **Tamaño**: Vertical (1024x1792) o cuadrado
- **Costo**: ~$0.08 por imagen (HD)
- **Recomendado para**: Máxima calidad y fidelidad al prompt

### 3. **DALL-E 2**
- **Proveedor**: OpenAI
- **Calidad**: Buena, más rápido
- **Tamaño**: Solo cuadrado (1024x1024)
- **Costo**: ~$0.02 por imagen
- **Recomendado para**: Pruebas rápidas y económicas

## 🔧 Configuración

### Paso 1: Obtener API Keys

#### Para Google Gemini:
1. Ve a: https://makersuite.google.com/app/apikey
2. Crea un proyecto si no tienes uno
3. Genera una API key
4. Copia la key (formato: `AIza...`)

#### Para OpenAI (DALL-E):
1. Ve a: https://platform.openai.com/api-keys
2. Crea una cuenta o inicia sesión
3. Ve a "API Keys" en el menú
4. Crea una nueva API key
5. Copia la key (formato: `sk-...`)

### Paso 2: Configurar en el Backend

Edita el archivo `/app/backend/.env`:

```bash
# Para usar Google Gemini
GEMINI_API_KEY=AIzaSy...tu-key-aqui

# Para usar DALL-E (OpenAI)
OPENAI_API_KEY=sk-proj-...tu-key-aqui

# Modelo por defecto (puedes cambiarlo)
DEFAULT_AI_MODEL=dalle
```

### Paso 3: Reiniciar el Backend

```bash
sudo supervisorctl restart backend
```

## 🎯 Cómo Usar

### Opción 1: Desde el Frontend

1. Ve a la página "Generate" en http://localhost:3000/generate
2. Llena el formulario de personalización (5 preguntas)
3. **Selecciona el modelo AI** en el dropdown:
   - Google Gemini
   - DALL-E 3
   - DALL-E 2
4. Haz clic en "Generate I'm Rich Image"

### Opción 2: Desde la API (cURL)

```bash
# Obtener token primero
TOKEN=$(curl -s -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"tu@email.com","password":"tupassword"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Generar imagen con DALL-E 3
curl -X POST http://localhost:8001/api/generate-image \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "customization": {
      "style": "elegant",
      "color_scheme": "gold",
      "elements": "cars",
      "mood": "luxurious",
      "additional_details": "Add a Ferrari and champagne"
    },
    "ai_model": "dalle"
  }'

# Generar imagen con Gemini
curl -X POST http://localhost:8001/api/generate-image \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "customization": {
      "style": "modern",
      "color_scheme": "black_gold",
      "elements": "watches",
      "mood": "sophisticated"
    },
    "ai_model": "gemini"
  }'
```

### Opción 3: Desde Python

```python
import requests

# Login
login_response = requests.post(
    "http://localhost:8001/api/auth/login",
    json={"email": "tu@email.com", "password": "tupassword"}
)
token = login_response.json()["access_token"]

# Generate image
headers = {"Authorization": f"Bearer {token}"}
payload = {
    "customization": {
        "style": "maximalist",
        "color_scheme": "platinum",
        "elements": "yachts",
        "mood": "extravagant",
        "additional_details": "Include a private jet in the background"
    },
    "ai_model": "dalle"  # Cambia a "gemini" o "dalle2"
}

response = requests.post(
    "http://localhost:8001/api/generate-image",
    headers=headers,
    json=payload
)

result = response.json()
print(f"Serial: {result['serial']}")
print(f"Image URL: {result['image_url_wallpaper']}")
```

## 🆕 Añadir Nuevos Modelos

Para añadir un nuevo modelo de IA (por ejemplo, Midjourney, Stable Diffusion, etc.):

### Paso 1: Añadir Configuración

Edita `/app/backend/services/ai_models_config.py`:

```python
AI_MODELS = {
    # ... modelos existentes ...
    
    "midjourney": {
        "name": "Midjourney",
        "provider": "Midjourney",
        "model_id": "v6",
        "env_key": "MIDJOURNEY_API_KEY",
        "description": "Artistic and creative image generation",
        "supported_sizes": ["1024x1024"],
        "default_size": "1024x1024",
        "cost_per_image": 0.05,
    },
}
```

### Paso 2: Implementar Lógica de Generación

Edita `/app/backend/services/image_generator.py`:

```python
async def generate_image(self, customization, model="gemini"):
    prompt = self.build_prompt(customization)
    
    # ... código existente ...
    
    elif model == "midjourney":
        # Tu implementación aquí
        api_key = os.getenv("MIDJOURNEY_API_KEY")
        # Llamar a la API de Midjourney
        # Retornar bytes de la imagen
        pass
```

### Paso 3: Añadir al Frontend

Edita `/app/frontend/src/pages/Generate.tsx`:

```tsx
<option value="midjourney">Midjourney (Artistic)</option>
```

## 📊 Comparación de Modelos

| Modelo | Calidad | Velocidad | Costo | Tamaño Vertical | Mejor Para |
|--------|---------|-----------|-------|-----------------|------------|
| Gemini | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $ | ✅ | Realismo y calidad |
| DALL-E 3 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | $$ | ✅ | Máxima fidelidad |
| DALL-E 2 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $ | ❌ | Pruebas rápidas |

## 🔍 Verificar Modelos Disponibles

Para ver qué modelos están configurados y disponibles:

```bash
curl http://localhost:8001/api/models | python3 -m json.tool
```

## 💡 Tips y Recomendaciones

1. **Para producción**: Usa Gemini o DALL-E 3 para mejor calidad
2. **Para pruebas**: Usa DALL-E 2 por su velocidad y bajo costo
3. **Prompts**: Sé específico en los detalles adicionales para mejores resultados
4. **API Keys**: Nunca compartas tus API keys públicamente
5. **Costos**: Monitorea tu uso en los dashboards de Google/OpenAI
6. **Rate Limits**: Ten en cuenta los límites de rate de cada proveedor

## 🐛 Troubleshooting

### Error: "API key not configured"
- Verifica que la API key esté en `/app/backend/.env`
- Reinicia el backend: `sudo supervisorctl restart backend`

### Error: "Insufficient quota"
- Tu API key ha alcanzado el límite
- Añade créditos en el dashboard del proveedor

### Error: "Invalid API key"
- Verifica que la API key sea correcta
- Asegúrate de que no tenga espacios o caracteres extra

### Imagen no se genera
- Revisa los logs: `tail -f /var/log/supervisor/backend.err.log`
- Verifica que el modelo seleccionado tenga API key configurada

## 📞 Soporte

Para más información sobre cada proveedor:
- **Google Gemini**: https://ai.google.dev/docs
- **OpenAI**: https://platform.openai.com/docs

---

**Última actualización**: 2024
