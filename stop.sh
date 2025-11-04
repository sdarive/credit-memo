#!/bin/bash

# Credit Memo Generator - Stop Script
# Stops both backend (Flask) and frontend (React) applications

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Stopping Credit Memo Generator...${NC}"

# Stop Backend
if [ -f .pids/backend.pid ]; then
    BACKEND_PID=$(cat .pids/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}Stopping backend (PID: $BACKEND_PID)...${NC}"
        kill $BACKEND_PID
        echo -e "${GREEN}Backend stopped${NC}"
    else
        echo -e "${RED}Backend process not running${NC}"
    fi
    rm .pids/backend.pid
else
    echo -e "${RED}Backend PID file not found${NC}"
fi

# Stop Frontend (kill npm and its child processes)
if [ -f .pids/frontend.pid ]; then
    FRONTEND_PID=$(cat .pids/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}Stopping frontend (PID: $FRONTEND_PID)...${NC}"
        # Kill the npm process and all its children
        pkill -P $FRONTEND_PID
        kill $FRONTEND_PID
        echo -e "${GREEN}Frontend stopped${NC}"
    else
        echo -e "${RED}Frontend process not running${NC}"
    fi
    rm .pids/frontend.pid
else
    echo -e "${RED}Frontend PID file not found${NC}"
fi

# Also kill any remaining node processes for the React dev server
echo -e "${YELLOW}Cleaning up any remaining React dev server processes...${NC}"
pkill -f "react-scripts start" 2>/dev/null && echo -e "${GREEN}Cleaned up React dev server${NC}" || echo -e "${YELLOW}No additional React processes found${NC}"

# Clean up .pids directory if empty
if [ -d .pids ] && [ -z "$(ls -A .pids)" ]; then
    rmdir .pids
fi

echo ""
echo -e "${GREEN}Credit Memo Generator stopped${NC}"
