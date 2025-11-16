# 🔓 Proyecto 100% Independiente

Este proyecto es **completamente independiente** y no depende de ninguna plataforma específica.

## ✅ Solo Dependencias Oficiales

### Librerías Usadas:
- **OpenAI** (`openai`) - Librería oficial de OpenAI para DALL-E
- **Google Generative AI** (`google-generativeai`) - Librería oficial de Google
- **FastAPI** - Framework web estándar
- **React** - Librería frontend estándar
- **SQLAlchemy** - ORM estándar para Python

### ❌ NO Dependencias:
- ❌ No depende de Emergent
- ❌ No depende de ninguna plataforma propietaria
- ❌ No hay código vendor-locked

## 🚀 Portable a Cualquier Servidor

Este proyecto puede ejecutarse en:
- ✅ Tu laptop/PC local
- ✅ AWS (EC2, Lambda, ECS)
- ✅ Google Cloud (Compute Engine, Cloud Run)
- ✅ Azure (VMs, App Service)
- ✅ DigitalOcean
- ✅ Heroku
- ✅ Vercel (frontend)
- ✅ Cualquier VPS con Python + Node.js

## 📦 Requisitos del Sistema

**Backend:**
- Python 3.11+
- pip
- 512MB RAM mínimo

**Frontend:**
- Node.js 18+
- yarn o npm
- 256MB RAM mínimo

## 🔧 Configuración Solo por Variables de Entorno

Todo se configura mediante archivos `.env`:

### Backend (`/app/backend/.env`):
```env
# AI Models - Elige el que quieras
OPENAI_API_KEY=your-key-here          # Para DALL-E
GEMINI_API_KEY=your-key-here          # Para Gemini (requiere Vertex AI)
DEFAULT_AI_MODEL=dalle                 # dalle, dalle2, o gemini

# Base de datos
DATABASE_URL=sqlite:///./imrich.db    # Puedes cambiar a PostgreSQL, MySQL, etc.

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256

# Otros servicios opcionales
STRIPE_SECRET_KEY=...                  # Si quieres pagos
SENDGRID_API_KEY=...                   # Si quieres emails
```

### Frontend (`/app/frontend/.env`):
```env
VITE_BACKEND_URL=http://localhost:8001  # URL de tu backend
```

## 🔄 Cambiar Proveedores de IA

### Usar DALL-E (OpenAI):
```env
OPENAI_API_KEY=sk-...
DEFAULT_AI_MODEL=dalle
```

### Usar Google Imagen (requiere Vertex AI):
```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
DEFAULT_AI_MODEL=gemini
```

### Añadir Más Modelos:

El archivo `/app/backend/services/image_generator.py` está estructurado para añadir fácilmente nuevos modelos:

```python
elif model == "midjourney":
    # Tu código aquí
    pass

elif model == "stable-diffusion":
    # Tu código aquí
    pass
```

## 🗄️ Cambiar Base de Datos

El proyecto usa SQLAlchemy, compatible con:

### SQLite (actual - incluido):
```env
DATABASE_URL=sqlite:///./imrich.db
```

### PostgreSQL:
```env
DATABASE_URL=postgresql://user:pass@localhost/imrich
```

### MySQL:
```env
DATABASE_URL=mysql://user:pass@localhost/imrich
```

### MongoDB:
```env
MONGO_URL=mongodb://localhost:27017/imrich
```

## 📤 Deployment

### Docker (Recomendado):

```dockerfile
# Dockerfile.backend
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

```dockerfile
# Dockerfile.frontend
FROM node:18-alpine
WORKDIR /app
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install
COPY frontend/ .
RUN yarn build
CMD ["yarn", "preview", "--host", "0.0.0.0", "--port", "3000"]
```

### Docker Compose:

```yaml
version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8001:8001"
    env_file:
      - backend/.env
    volumes:
      - ./generated:/app/generated
      
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:3000"
    env_file:
      - frontend/.env
    depends_on:
      - backend
```

### AWS (EC2 / ECS):
1. Sube los Dockerfiles
2. Configura las variables de entorno
3. Expone los puertos necesarios

### Vercel (Frontend):
```bash
cd frontend
vercel --prod
```

### Heroku:
```bash
# Backend
heroku create imrich-backend
git push heroku master

# Frontend  
heroku create imrich-frontend
git push heroku master
```

## 🔐 Seguridad

- ✅ API keys solo en archivos `.env` (no en código)
- ✅ `.env` en `.gitignore` (nunca en Git)
- ✅ Solo `.env.example` en el repositorio
- ✅ JWT para autenticación
- ✅ CORS configurado correctamente
- ✅ Passwords hasheados con bcrypt

## 📊 Escalabilidad

### Horizontal Scaling:
- Backend: Múltiples instancias detrás de un load balancer
- Frontend: CDN + múltiples servidores
- Base de datos: Replica sets / Read replicas

### Vertical Scaling:
- Aumenta CPU/RAM según necesidad
- Optimiza queries de base de datos
- Implementa caching (Redis)

## 🎯 Independencia Garantizada

**Promesa de Independencia:**
1. ✅ No hay código propietario
2. ✅ Solo librerías open source o APIs públicas oficiales
3. ✅ Funciona en cualquier infraestructura
4. ✅ Migrable en cualquier momento
5. ✅ Sin vendor lock-in

**¿Cómo verificarlo?**
```bash
# Ver todas las dependencias del backend
cat backend/requirements.txt

# Ver todas las dependencias del frontend
cat frontend/package.json

# Buscar "emergent" en el código (no debería aparecer)
grep -r "emergent" backend/ frontend/ --exclude-dir=node_modules
```

---

## 🆘 Soporte

Este proyecto no depende de ninguna plataforma. Para ayuda:
- **Código**: https://github.com/Santiagorr88/richAI
- **Documentación oficial**:
  - OpenAI: https://platform.openai.com/docs
  - Google AI: https://ai.google.dev/docs
  - FastAPI: https://fastapi.tiangolo.com
  - React: https://react.dev

---

**Tu proyecto, tu infraestructura, tu control total. 🔓✨**
