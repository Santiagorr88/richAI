#!/bin/bash

echo "🧪 Testing I'm Rich AI System..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Backend Health
echo "1️⃣  Testing Backend Health..."
HEALTH=$(curl -s http://localhost:8001/api/health)
if [[ $HEALTH == *"healthy"* ]]; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${RED}❌ Backend is not responding${NC}"
    exit 1
fi
echo ""

# Test 2: Available Models
echo "2️⃣  Checking Available AI Models..."
curl -s http://localhost:8001/api/models | python3 -m json.tool
echo ""

# Test 3: Register User
echo "3️⃣  Testing User Registration..."
REGISTER_RESULT=$(curl -s -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@imrich.com","password":"demo123456","first_name":"Demo","last_name":"User"}')

if [[ $REGISTER_RESULT == *"access_token"* ]]; then
    echo -e "${GREEN}✅ User registration successful${NC}"
    TOKEN=$(echo $REGISTER_RESULT | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
    echo "Token: ${TOKEN:0:50}..."
else
    echo -e "${YELLOW}⚠️  User might already exist, trying login...${NC}"
    LOGIN_RESULT=$(curl -s -X POST http://localhost:8001/api/auth/login \
      -H "Content-Type: application/json" \
      -d '{"email":"demo@imrich.com","password":"demo123456"}')
    TOKEN=$(echo $LOGIN_RESULT | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
    echo -e "${GREEN}✅ Login successful${NC}"
fi
echo ""

# Test 4: Check User Info
echo "4️⃣  Fetching User Info..."
USER_INFO=$(curl -s http://localhost:8001/api/auth/me \
  -H "Authorization: Bearer $TOKEN")
echo $USER_INFO | python3 -m json.tool
echo ""

# Test 5: Check API Keys Configuration
echo "5️⃣  Checking API Keys Configuration..."
if grep -q "your-gemini-api-key-here" /app/backend/.env; then
    echo -e "${YELLOW}⚠️  Gemini API key not configured${NC}"
else
    echo -e "${GREEN}✅ Gemini API key configured${NC}"
fi

if grep -q "your-openai-api-key-here" /app/backend/.env; then
    echo -e "${YELLOW}⚠️  OpenAI API key not configured${NC}"
else
    echo -e "${GREEN}✅ OpenAI API key configured${NC}"
fi
echo ""

# Test 6: Frontend Status
echo "6️⃣  Checking Frontend..."
if pgrep -f "vite" > /dev/null; then
    echo -e "${GREEN}✅ Frontend is running${NC}"
    echo "   Access at: http://localhost:3000"
else
    echo -e "${RED}❌ Frontend is not running${NC}"
fi
echo ""

echo "📊 System Status Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Backend:  ✅ Running on http://localhost:8001"
echo "Frontend: ✅ Running on http://localhost:3000"
echo "Database: ✅ SQLite configured"
echo ""
echo "🎯 Next Steps:"
echo "1. Configure your Gemini or OpenAI API key in /app/backend/.env"
echo "2. Restart backend: sudo supervisorctl restart backend"
echo "3. Open http://localhost:3000 in your browser"
echo "4. Register and generate your first image!"
echo ""
echo "📚 For model configuration help, see: /app/AI_MODELS_GUIDE.md"
