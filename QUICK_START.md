# 🚀 Quick Start - I'm Rich AI

## ⚡ Inicio Rápido (3 pasos)

### 1. Configurar API Key

Edita `/app/backend/.env` y añade tu API key:

**Opción A: Usar DALL-E (OpenAI)**
```env
OPENAI_API_KEY=your-openai-api-key-here
DEFAULT_AI_MODEL=dalle
```

**Opción B: Usar Gemini (Google)**
```env
GEMINI_API_KEY=your-gemini-api-key-here
DEFAULT_AI_MODEL=gemini
```

> **Nota**: Copia desde `.env.example` y añade tus propias API keys

### 2. Reiniciar Backend

```bash
sudo supervisorctl restart backend
```

### 3. Abrir la App

Abre en tu navegador: **http://localhost:3000**

---

## 🎮 Usar la Aplicación

### Paso 1: Registro
- Ve a http://localhost:3000
- Haz clic en "Register"
- Crea tu cuenta con email y contraseña

### Paso 2: Generar Imagen
- Haz clic en "Generate I'm Rich Image"
- Responde las 5 preguntas de personalización:
  1. **Estilo**: minimalist, maximalist, elegant, modern, classic
  2. **Esquema de color**: gold, silver, black & gold, rose gold, platinum
  3. **Elementos**: cars, watches, jewelry, yachts, mansions
  4. **Mood**: luxurious, extravagant, sophisticated, bold, subtle
  5. **Detalles adicionales**: (opcional) texto libre
- Selecciona el **modelo AI**:
  - **DALL-E 3**: Ultra HD, mejor calidad (OpenAI)
  - **DALL-E 2**: Más rápido y económico (OpenAI)
  - **Gemini**: Alta calidad (Google)
- Haz clic en "Generate"

### Paso 3: Ver tus Imágenes
- Ve a "My Images" en el menú
- Verás todas tus imágenes generadas
- Descarga 2 versiones:
  - **Wallpaper**: Imagen limpia para fondo de pantalla
  - **Verified**: Imagen con QR code y serial number

### Paso 4: Verificar Autenticidad
- Copia el serial number
- Ve a http://localhost:3000/verify
- Pega el serial number
- El sistema verificará si es auténtico

---

## 🔄 Cambiar entre Modelos AI

### En el Frontend (interfaz web):
1. Ve a la página "Generate"
2. Selecciona el modelo en el dropdown "AI Model"
3. Genera la imagen

### Cambiar el modelo por defecto:
Edita `/app/backend/.env`:
```env
DEFAULT_AI_MODEL=dalle  # o "gemini" o "dalle2"
```

---

## 📊 Comandos Útiles

### Ver estado de servicios
```bash
sudo supervisorctl status
```

### Ver logs del backend
```bash
tail -f /var/log/supervisor/backend.out.log
tail -f /var/log/supervisor/backend.err.log
```

### Reiniciar todo
```bash
sudo supervisorctl restart all
```

### Probar el sistema
```bash
/app/test_system.sh
```

---

## 🎯 Ejemplos de Uso

### Ejemplo 1: Imagen con Ferrari y oro
```
Style: elegant
Color: gold
Elements: cars
Mood: luxurious
Details: "Ferrari 488, golden sunset, luxury lifestyle"
Model: dalle
```

### Ejemplo 2: Imagen minimalista con reloj
```
Style: minimalist
Color: platinum
Elements: watches
Mood: sophisticated
Details: "Rolex watch, clean background"
Model: gemini
```

---

## ❓ FAQ

**P: ¿Cuál modelo debo usar?**
- Para máxima calidad: DALL-E 3 o Gemini
- Para pruebas rápidas: DALL-E 2

**P: ¿Cuánto cuesta cada imagen?**
- DALL-E 2: ~$0.02
- Gemini: ~$0.04
- DALL-E 3: ~$0.08

**P: ¿Dónde obtengo las API keys?**
- OpenAI: https://platform.openai.com/api-keys
- Google Gemini: https://makersuite.google.com/app/apikey

---

## 📚 Más Documentación

- **README completo**: `/app/README.md`
- **Guía de modelos AI**: `/app/AI_MODELS_GUIDE.md`
- **API Documentation**: http://localhost:8001/docs
- **Git Setup**: `/app/GIT_SETUP.md`

---

**¡Listo para generar imágenes de lujo! 💎✨**
