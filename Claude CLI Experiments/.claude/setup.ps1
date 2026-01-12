# Perplexity Research Integration Setup for Claude Code Max CLI (Windows)
# Combines multiagent orchestration with research capabilities

$ErrorActionPreference = "Stop"

Write-Host "=========================================================================" -ForegroundColor Blue
Write-Host "  Claude Code Max - Multimodal Research Integration Setup" -ForegroundColor Blue
Write-Host "=========================================================================" -ForegroundColor Blue
Write-Host ""

# Step 1: Check Python
Write-Host "[1/7] Checking Python installation..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "✗ Python not found" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from python.org"
    exit 1
}

$pythonVersion = & python --version 2>&1
Write-Host "✓ $pythonVersion detected" -ForegroundColor Green
Write-Host ""

# Step 2: Create virtual environment
Write-Host "[2/7] Creating virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    & python -m venv .venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "  Virtual environment already exists" -ForegroundColor Blue
}
Write-Host ""

# Step 3: Activate virtual environment
Write-Host "[3/7] Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Step 4: Install Python dependencies
Write-Host "[4/7] Installing Python dependencies..." -ForegroundColor Yellow
& python -m pip install --upgrade pip --quiet
& python -m pip install playwright aiohttp --quiet
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Step 5: Install Playwright browsers
Write-Host "[5/7] Installing Playwright Chromium browser..." -ForegroundColor Yellow
& playwright install chromium
Write-Host "✓ Playwright Chromium installed" -ForegroundColor Green
Write-Host ""

# Step 6: Create directory structure
Write-Host "[6/7] Setting up directory structure..." -ForegroundColor Yellow
$directories = @(
    ".claude\sessions",
    ".claude\commands",
    ".claude\agents",
    ".claude\config",
    ".claude\docs\adrs",
    ".claude\workflows",
    ".claude\memory\vector_store"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

Write-Host "✓ Directory structure created" -ForegroundColor Green
Write-Host ""

# Step 7: Configure .gitignore
Write-Host "[7/7] Configuring .gitignore..." -ForegroundColor Yellow
$gitignoreEntries = @(
    ".claude/sessions/*.json",
    ".claude/perplexity_bridge.log",
    ".claude/memory/vector_store/*",
    ".venv/",
    "*.pyc",
    "__pycache__/"
)

if (Test-Path ".gitignore") {
    $currentGitignore = Get-Content .gitignore -Raw
    foreach ($entry in $gitignoreEntries) {
        if ($currentGitignore -notmatch [regex]::Escape($entry)) {
            Add-Content .gitignore "`n$entry"
        }
    }
    Write-Host "✓ .gitignore updated" -ForegroundColor Green
} else {
    $gitignoreEntries | Out-File .gitignore -Encoding utf8
    Write-Host "✓ .gitignore created" -ForegroundColor Green
}
Write-Host ""

# Test installation
Write-Host "=========================================================================" -ForegroundColor Blue
Write-Host "Testing installation..." -ForegroundColor Blue
Write-Host "=========================================================================" -ForegroundColor Blue
Write-Host ""

try {
    & python .claude\perplexity_bridge.py --help | Out-Null
    Write-Host "✓ Perplexity bridge is working" -ForegroundColor Green
} catch {
    Write-Host "✗ Perplexity bridge test failed" -ForegroundColor Red
    exit 1
}

try {
    & python .claude\config\agent_orchestrator.py --help | Out-Null
    Write-Host "✓ Agent orchestrator is working" -ForegroundColor Green
} catch {
    Write-Host "✗ Agent orchestrator test failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=========================================================================" -ForegroundColor Blue
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "=========================================================================" -ForegroundColor Blue
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Blue
Write-Host ""
Write-Host "1. Authenticate with Perplexity (one-time setup):"
Write-Host "   python .claude\perplexity_bridge.py --check-auth --visible"
Write-Host ""
Write-Host "2. Test a research query:"
Write-Host "   /research artificial intelligence best practices 2024"
Write-Host ""
Write-Host "3. Create a smart project plan:"
Write-Host "   /smart-plan"
Write-Host ""
Write-Host "4. Debug with research assistance:"
Write-Host "   /smart-debug"
Write-Host ""
Write-Host "5. Optimize code with research:"
Write-Host "   /smart-optimize"
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Blue
Write-Host "   .claude\README.md - Complete integration guide"
Write-Host "   .claude\commands\ - Slash command documentation"
Write-Host "   .claude\agents\ - Agent configuration details"
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Blue
Write-Host "   .claude\config\integration_config.json - System configuration"
Write-Host ""
Write-Host "Important:" -ForegroundColor Yellow
Write-Host "   - First research query requires browser authentication"
Write-Host "   - Session lasts 23 hours, then auto-refreshes"
Write-Host "   - Query results cached for 1 hour to optimize performance"
Write-Host ""
Write-Host "=========================================================================" -ForegroundColor Blue
