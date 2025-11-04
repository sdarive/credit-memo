#!/bin/bash

# Credit Memo Generator - Start Script
# Starts both backend (Flask) and frontend (React) applications

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Credit Memo Generator...${NC}"

# Check if .pids directory exists, create if not
mkdir -p .pids

# Start Backend (Flask)
echo -e "${BLUE}Starting backend (Flask)...${NC}"
cd backend
python3 app.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../.pids/backend.pid
cd ..
echo -e "${GREEN}Backend started (PID: $BACKEND_PID)${NC}"

# Wait a moment for backend to initialize
sleep 2

# Start Frontend (React)
echo -e "${BLUE}Starting frontend (React)...${NC}"
cd frontend
npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../.pids/frontend.pid
cd ..
echo -e "${GREEN}Frontend started (PID: $FRONTEND_PID)${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Credit Memo Generator is starting up!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Backend (Flask):  http://localhost:5000"
echo -e "Frontend (React): http://localhost:3000"
echo ""
echo -e "Logs:"
echo -e "  Backend:  logs/backend.log"
echo -e "  Frontend: logs/frontend.log"
echo ""
echo -e "To stop both applications, run: ${BLUE}./stop.sh${NC}"
echo ""
