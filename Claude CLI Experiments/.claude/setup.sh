#!/bin/bash
# Perplexity Research Integration Setup for Claude Code Max CLI
# Combines multiagent orchestration with research capabilities

set -e

echo "========================================================================="
echo "  Claude Code Max - Multimodal Research Integration Setup"
echo "========================================================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
fi

echo -e "${BLUE}Detected OS: $OS${NC}"
echo ""

# Step 1: Check Python
echo -e "${YELLOW}[1/7] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 not found${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"
echo ""

# Step 2: Create virtual environment
echo -e "${YELLOW}[2/7] Creating virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${BLUE}  Virtual environment already exists${NC}"
fi
echo ""

# Step 3: Activate virtual environment
echo -e "${YELLOW}[3/7] Activating virtual environment...${NC}"
if [[ "$OS" == "windows" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Step 4: Install Python dependencies
echo -e "${YELLOW}[4/7] Installing Python dependencies...${NC}"
pip install --upgrade pip --quiet
pip install playwright aiohttp --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 5: Install Playwright browsers
echo -e "${YELLOW}[5/7] Installing Playwright Chromium browser...${NC}"
playwright install chromium
echo -e "${GREEN}✓ Playwright Chromium installed${NC}"
echo ""

# Step 6: Create directory structure
echo -e "${YELLOW}[6/7] Setting up directory structure...${NC}"
mkdir -p .claude/sessions
mkdir -p .claude/commands
mkdir -p .claude/agents
mkdir -p .claude/config
mkdir -p .claude/docs/adrs
mkdir -p .claude/workflows
mkdir -p .claude/memory/vector_store

# Make scripts executable
chmod +x .claude/perplexity_bridge.py 2>/dev/null || true
chmod +x .claude/config/agent_orchestrator.py 2>/dev/null || true

echo -e "${GREEN}✓ Directory structure created${NC}"
echo ""

# Step 7: Create .gitignore entries
echo -e "${YELLOW}[7/7] Configuring .gitignore...${NC}"
GITIGNORE_ENTRIES=(
    ".claude/sessions/*.json"
    ".claude/perplexity_bridge.log"
    ".claude/memory/vector_store/*"
    ".venv/"
    "*.pyc"
    "__pycache__/"
)

if [ -f ".gitignore" ]; then
    for entry in "${GITIGNORE_ENTRIES[@]}"; do
        if ! grep -q "^$entry$" .gitignore; then
            echo "$entry" >> .gitignore
        fi
    done
    echo -e "${GREEN}✓ .gitignore updated${NC}"
else
    printf "%s\n" "${GITIGNORE_ENTRIES[@]}" > .gitignore
    echo -e "${GREEN}✓ .gitignore created${NC}"
fi
echo ""

# Test installation
echo "========================================================================="
echo -e "${BLUE}Testing installation...${NC}"
echo "========================================================================="
echo ""

python3 .claude/perplexity_bridge.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Perplexity bridge is working${NC}"
else
    echo -e "${RED}✗ Perplexity bridge test failed${NC}"
    exit 1
fi

python3 .claude/config/agent_orchestrator.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Agent orchestrator is working${NC}"
else
    echo -e "${RED}✗ Agent orchestrator test failed${NC}"
    exit 1
fi

echo ""
echo "========================================================================="
echo -e "${GREEN}  Setup Complete!${NC}"
echo "========================================================================="
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Authenticate with Perplexity (one-time setup):"
echo "   python .claude/perplexity_bridge.py --check-auth --visible"
echo ""
echo "2. Test a research query:"
echo "   /research artificial intelligence best practices 2024"
echo ""
echo "3. Create a smart project plan:"
echo "   /smart-plan"
echo ""
echo "4. Debug with research assistance:"
echo "   /smart-debug"
echo ""
echo "5. Optimize code with research:"
echo "   /smart-optimize"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "   .claude/README.md - Complete integration guide"
echo "   .claude/commands/ - Slash command documentation"
echo "   .claude/agents/ - Agent configuration details"
echo ""
echo -e "${BLUE}Configuration:${NC}"
echo "   .claude/config/integration_config.json - System configuration"
echo ""
echo -e "${YELLOW}Important:${NC}"
echo "   - First research query requires browser authentication"
echo "   - Session lasts 23 hours, then auto-refreshes"
echo "   - Query results cached for 1 hour to optimize performance"
echo ""
echo "========================================================================="
