# Git Setup Guide - I'm Rich AI

## 🔒 Problema de Seguridad Resuelto

Los archivos `.env` contienen información sensible (API keys) y **NO deben** estar en Git.

### ✅ Lo que he hecho:

1. **Creado archivos .env.example**:
   - `/app/backend/.env.example` - Plantilla para backend
   - `/app/frontend/.env.example` - Plantilla para frontend
   
2. **Actualizado .gitignore**:
   - Los archivos `.env` ya están ignorados
   - Solo se suben los archivos `.env.example`

3. **Archivos .env locales**:
   - Permanecen en tu máquina con tus API keys reales
   - NO se subirán a GitHub

---

## 🔧 Configuración para otros desarrolladores

Cuando alguien clone tu repositorio:

```bash
# 1. Clonar el repositorio
git clone https://github.com/Santiagorr88/richAI.git
cd richAI

# 2. Copiar los archivos .env.example
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 3. Editar los archivos .env con sus propias API keys
nano backend/.env   # Añadir GEMINI_API_KEY o OPENAI_API_KEY
nano frontend/.env  # Configurar VITE_BACKEND_URL si es necesario

# 4. Instalar dependencias y ejecutar
cd backend && pip install -r requirements.txt
cd ../frontend && yarn install
sudo supervisorctl restart all
```

---

## 🚫 Problema de Permisos de Git (Error 403)

El error que recibiste:
```
remote: Permission to Santiagorr88/richAI.git denied to Santiagorr88.
fatal: unable to access 'https://github.com/Santiagorr88/richAI.git/': The requested URL returned error: 403
```

Esto significa que **no tienes permisos** configurados correctamente en GitHub desde esta máquina.

### Soluciones:

#### Opción 1: Usar GitHub Personal Access Token (Recomendado)

1. **Crear un Token**:
   - Ve a: https://github.com/settings/tokens
   - Click en "Generate new token (classic)"
   - Selecciona scopes: `repo` (acceso completo a repositorios)
   - Genera y **copia el token** (solo se muestra una vez)

2. **Configurar el token**:
   ```bash
   # Actualizar la URL del remote para usar el token
   cd /app
   git remote set-url origin https://TU-TOKEN@github.com/Santiagorr88/richAI.git
   
   # O con tu username:
   git remote set-url origin https://Santiagorr88:TU-TOKEN@github.com/Santiagorr88/richAI.git
   ```

3. **Hacer push**:
   ```bash
   git add .
   git commit -m "Added I'm Rich AI application"
   git push origin main
   ```

#### Opción 2: Usar SSH (Más seguro)

1. **Generar SSH key** (si no tienes una):
   ```bash
   ssh-keygen -t ed25519 -C "tu-email@example.com"
   cat ~/.ssh/id_ed25519.pub  # Copiar esta clave
   ```

2. **Añadir la clave a GitHub**:
   - Ve a: https://github.com/settings/keys
   - Click "New SSH key"
   - Pega la clave pública

3. **Cambiar a SSH**:
   ```bash
   cd /app
   git remote set-url origin git@github.com:Santiagorr88/richAI.git
   git push origin main
   ```

#### Opción 3: Usar la interfaz de Emergent

Si estás usando Emergent Agent, usa la función **"Save to GitHub"** en la interfaz:
- Esto maneja automáticamente la autenticación
- No necesitas configurar tokens manualmente

---

## 📦 Qué se sube a Git

### ✅ Se DEBE subir:
- Código fuente (`*.py`, `*.ts`, `*.tsx`, etc.)
- Archivos de configuración (`package.json`, `requirements.txt`, etc.)
- Archivos `.env.example` (plantillas sin datos sensibles)
- Documentación (`README.md`, `*.md`)

### ❌ NO se debe subir:
- Archivos `.env` (contienen API keys)
- `node_modules/` (dependencias de Node)
- `__pycache__/` (archivos compilados de Python)
- Imágenes generadas en `/generated/`
- Base de datos `*.db`
- Logs `*.log`

Todo esto ya está configurado en `.gitignore`.

---

## 🔄 Workflow Recomendado

```bash
# 1. Hacer cambios en tu código
# ...

# 2. Revisar qué cambió
git status
git diff

# 3. Agregar cambios
git add .

# 4. Commit
git commit -m "Descripción clara de los cambios"

# 5. Push (necesitas permisos configurados)
git push origin main
```

---

## 🛡️ Seguridad de API Keys

### Si accidentalmente subiste un .env con API keys:

1. **Inmediatamente revocar las API keys** en:
   - OpenAI: https://platform.openai.com/api-keys
   - Google: https://console.cloud.google.com/apis/credentials

2. **Generar nuevas API keys**

3. **Remover el archivo del historial de Git**:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch backend/.env" \
     --prune-empty --tag-name-filter cat -- --all
   
   git push origin --force --all
   ```

4. **Actualizar tus archivos .env locales** con las nuevas keys

---

## 📝 Buenas Prácticas

1. **Nunca** commits archivos `.env` directamente
2. **Siempre** usa `.env.example` como plantilla
3. **Rota** las API keys regularmente
4. **Usa** diferentes keys para desarrollo y producción
5. **Considera** usar servicios de gestión de secretos (AWS Secrets Manager, Google Secret Manager, etc.) para producción

---

## 🆘 Si necesitas ayuda

- **GitHub Docs**: https://docs.github.com/en/authentication
- **Git Docs**: https://git-scm.com/doc
- **Emergent Support**: Usa el support_agent en el chat

---

**Tus API keys están seguras y el proyecto está listo para compartir en GitHub! 🔒✅**
