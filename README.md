# I'm Rich AI 💎

A full-stack web application that generates AI-certified luxury images with unique serial numbers for authenticity verification.

## 🎯 Features

- **AI Image Generation**: Powered by Google Gemini for hyper-realistic luxury imagery
- **Unique Serial Numbers**: Each image gets a unique serial for authentication
- **Dual Image Versions**: 
  - Verified version with QR code and serial number
  - Clean wallpaper version for actual use
- **Authentication**: JWT-based user authentication (OAuth ready for Google/Apple)
- **User Dashboard**: View all your generated images with serial numbers
- **Verification System**: Public verification page to check image authenticity
- **Payment Ready**: Prepared for Stripe integration (card + Apple Pay)
- **Email Ready**: Prepared for SendGrid integration

## 🛠️ Tech Stack

### Backend
- **FastAPI** (Python 3.11+)
- **SQLite** + SQLAlchemy (Database)
- **Google Gemini** (AI Image Generation)
- **Pillow** (Image Composition)
- **QRCode** (QR Code Generation)
- **JWT** (Authentication)

### Frontend
- **React** + **TypeScript**
- **Vite** (Build Tool)
- **React Router** (Routing)
- **Axios** (HTTP Client)
- **Tailwind CSS** (Styling)

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+ & Yarn
- Google Gemini API Key

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
cd /app
```

### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Install emergentintegrations library
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/

# Configure environment variables
# Edit .env file and add your Google Gemini API key
nano .env
```

**Important Environment Variables in `/app/backend/.env`:**

```env
# Google Gemini API (REQUIRED)
GEMINI_API_KEY=your-gemini-api-key-here

# Database
DATABASE_URL=sqlite:///./imrich.db

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production-min-32-chars
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Base URL for QR codes
BASE_URL=http://localhost:3000

# TODO: Configure when ready
# SENDGRID_API_KEY=your-sendgrid-api-key
# STRIPE_SECRET_KEY=your-stripe-secret-key
# GOOGLE_CLIENT_ID=your-google-client-id
# GOOGLE_CLIENT_SECRET=your-google-client-secret
# APPLE_CLIENT_ID=your-apple-client-id
```

### 3. Frontend Setup

```bash
cd /app/frontend

# Install dependencies
yarn install

# Environment is already configured in .env
# VITE_BACKEND_URL=http://localhost:8001
```

### 4. Running the Application

#### Using Supervisor (Recommended - both services in background):

```bash
# Start both backend and frontend
sudo supervisorctl restart all

# Check status
sudo supervisorctl status

# View logs
tail -f /var/log/supervisor/backend.out.log
tail -f /var/log/supervisor/frontend.out.log
```

#### Manual Mode (for development):

```bash
# Terminal 1 - Backend
cd /app/backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2 - Frontend
cd /app/frontend
yarn dev --host 0.0.0.0 --port 3000
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

## 📖 User Flow

### 1. Registration / Login
- User creates an account with email and password
- JWT token is issued for authentication

### 2. Image Generation
- User navigates to "Generate" page
- Answers 5 customization questions:
  1. Style (minimalist, maximalist, elegant, modern, classic)
  2. Color Scheme (gold, silver, black & gold, rose gold, platinum)
  3. Elements (cars, watches, jewelry, yachts, mansions)
  4. Mood (luxurious, extravagant, sophisticated, bold, subtle)
  5. Additional details (optional text input)
- Selects AI model (Gemini is default)
- Clicks "Generate"

### 3. Image Processing (Backend)
- Generates unique serial number (format: `RICH-YYYYMMDDHHMMSS-XXXXXXXX`)
- Calls Google Gemini API with custom prompt
- Receives AI-generated image
- Generates QR code linking to verification page
- Creates 2 image versions:
  - **Verified**: AI image + QR code + serial text (bottom-left)
  - **Wallpaper**: Clean AI image without QR/serial
- Saves both images to `/app/generated/` directory
- Stores record in SQLite database

### 4. Dashboard
- User sees all their generated images
- Can download both versions
- Can copy serial numbers
- Can verify authenticity

### 5. Verification
- Anyone can visit `/verify/:serial`
- Enter serial number or scan QR code
- System checks database
- Shows authenticity result with image preview

## 🗄️ Database Schema

### Users Table
```sql
- id (Primary Key)
- email (Unique)
- password_hash
- first_name
- last_name
- created_at
```

### Images Table
```sql
- id (Primary Key)
- user_id (Foreign Key)
- serial (Unique Index)
- image_path_verified
- image_path_wallpaper
- prompt (Text - AI prompt used)
- customization (JSON - user choices)
- created_at
- payment_status (pending/completed/failed)
```

### Payments Table
```sql
- id (Primary Key)
- user_id (Foreign Key)
- image_id (Foreign Key)
- amount
- currency
- status (pending/completed/failed/refunded)
- payment_intent_id (Stripe ID)
- created_at
- completed_at
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Image Generation
- `POST /api/generate-image` - Generate AI image (requires auth)
- `GET /api/my-images` - Get user's images (requires auth)
- `GET /api/images/{filename}` - Serve image file
- `GET /api/verify/{serial}` - Verify image authenticity (public)

### Payments (TODO)
- `POST /api/payments/create-intent` - Create Stripe payment intent
- `POST /api/payments/webhook` - Handle Stripe webhooks
- `GET /api/payments/{payment_id}` - Get payment details

## 🔧 Configuration & Integration TODOs

### 1. Stripe Payment Integration

**Steps to configure:**

1. Create Stripe account at https://stripe.com
2. Get API keys from Stripe Dashboard
3. Add to `/app/backend/.env`:
   ```env
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_PUBLISHABLE_KEY=pk_test_...
   STRIPE_WEBHOOK_SECRET=whsec_...
   ```
4. Uncomment payment endpoints in `server.py`
5. Install: `pip install stripe`
6. Implement payment intent creation in `/api/payments/create-intent`
7. Implement webhook handler in `/api/payments/webhook`
8. Update frontend payment flow in Generate page

**Apple Pay**: Works automatically through Stripe once configured

### 2. SendGrid Email Integration

**Steps to configure:**

1. Create SendGrid account at https://sendgrid.com
2. Create API key with mail sending permissions
3. Add to `/app/backend/.env`:
   ```env
   SENDGRID_API_KEY=SG.xxx
   FROM_EMAIL=noreply@imrich.app
   ```
4. Install: `pip install sendgrid`
5. Uncomment `send_email_with_images` function in `server.py`
6. Implement email template with both image attachments
7. Call after successful image generation

### 3. Google OAuth

**Steps to configure:**

1. Go to Google Cloud Console
2. Create OAuth 2.0 credentials
3. Add authorized redirect URI: `http://localhost:8001/api/auth/google/callback`
4. Add to `/app/backend/.env`:
   ```env
   GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=xxx
   ```
5. Uncomment Google OAuth endpoints in `server.py`
6. Implement OAuth flow (redirect, callback, token exchange)
7. Add Google login button in frontend Login/Register pages

### 4. Apple OAuth

**Steps to configure:**

1. Apple Developer Account required ($99/year)
2. Create App ID and Services ID
3. Generate private key for Sign in with Apple
4. Add to `/app/backend/.env`:
   ```env
   APPLE_CLIENT_ID=com.your.app
   APPLE_TEAM_ID=XXXXXXXXXX
   APPLE_KEY_ID=XXXXXXXXXX
   APPLE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----...
   ```
5. Uncomment Apple OAuth endpoints in `server.py`
6. Implement Apple OAuth flow
7. Add Apple login button in frontend

## 🧪 Testing

### Backend Testing

```bash
# Health check
curl http://localhost:8001/api/health

# Register user
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Generate image (requires token)
curl -X POST http://localhost:8001/api/generate-image \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "customization": {
      "style": "elegant",
      "color_scheme": "gold",
      "elements": "cars",
      "mood": "luxurious"
    }
  }'
```

### Frontend Testing

1. Open http://localhost:3000
2. Register a new account
3. Login
4. Generate an image with custom options
5. Check Dashboard for generated images
6. Download both versions
7. Test verification page

## 📁 Project Structure

```
/app/
├── backend/
│   ├── server.py              # Main FastAPI application
│   ├── database.py            # Database configuration
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── auth.py                # JWT authentication
│   ├── services/
│   │   ├── image_generator.py # Gemini API integration
│   │   ├── serial_generator.py # Serial number generation
│   │   ├── qr_generator.py    # QR code generation
│   │   └── image_composer.py  # Image composition with Pillow
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── api/               # API client functions
│   │   ├── components/        # React components
│   │   ├── context/           # React context (Auth)
│   │   ├── pages/             # Page components
│   │   ├── App.tsx            # Main App component
│   │   └── main.tsx           # Entry point
│   ├── package.json           # Node dependencies
│   ├── tailwind.config.js     # Tailwind configuration
│   └── .env                   # Frontend environment variables
│
├── generated/                 # Generated images directory
└── README.md                  # This file
```

## 🎨 Customization Options

### AI Prompt Customization

Edit `/app/backend/services/image_generator.py` to modify how prompts are built based on user choices.

### Styling

- **Frontend**: Edit Tailwind config in `/app/frontend/tailwind.config.js`
- **Components**: All components in `/app/frontend/src/` use Tailwind classes

### Image Composition

Edit `/app/backend/services/image_composer.py` to change:
- QR code position and size
- Serial number text styling
- Image format and quality

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check logs
tail -f /var/log/supervisor/backend.err.log

# Common issues:
# 1. Missing GEMINI_API_KEY in .env
# 2. Database permissions
# 3. Missing Python packages
```

### Frontend won't start

```bash
# Check logs
tail -f /var/log/supervisor/frontend.err.log

# Common issues:
# 1. Port already in use
# 2. Node modules not installed (run: cd frontend && yarn install)
```

### Image generation fails

```bash
# Check:
# 1. GEMINI_API_KEY is correct and has quota
# 2. /app/generated/ directory exists and is writable
# 3. Backend logs for detailed error messages
```

## 📝 License

This project is a demonstration/prototype. Configure all TODO items before production use.

## 🤝 Contributing

This is a prototype. Key areas for contribution:
1. Stripe payment integration
2. SendGrid email integration
3. OAuth implementations (Google, Apple)
4. Frontend UI/UX improvements
5. Additional AI model support (DALL-E)

---

**Built with FastAPI, React, and Google Gemini** 🚀
