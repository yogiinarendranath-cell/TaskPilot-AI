$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
chcp 65001 > $null
$env:PYTHONUTF8 = "1"

if (-not (Test-Path .\.venv\Scripts\Activate.ps1)) {
    Write-Host "Creating venv..." -ForegroundColor Cyan
    py -3 -m venv .venv
}
. .\.venv\Scripts\Activate.ps1

Write-Host "`n=== Installing project ===" -ForegroundColor Cyan
python -m pip install -e . -q
python -m pip install pytest -q

Write-Host "`n=== Running tests ===" -ForegroundColor Cyan
pytest -q
if ($LASTEXITCODE -ne 0) { throw "tests failed" }

Write-Host "`n=== Success demo (should exit 0) ===" -ForegroundColor Cyan
python -m taskpilot run --task examples\task_demo.json --workspace .\workspace --out .\output.csv --logs .\logs
if ($LASTEXITCODE -ne 0) { throw "success demo failed" }

Write-Host "`n=== Failure demo (should exit 1) ===" -ForegroundColor Cyan
python -m taskpilot run --task examples\task_failure.json --workspace .\workspace --out .\output_fail.csv --logs .\logs_fail
if ($LASTEXITCODE -ne 1) { throw "failure demo did not exit 1" }

Write-Host "`n=== VERIFIED ===" -ForegroundColor Green
Write-Host "output.csv:" -ForegroundColor Green
Get-Content .\output.csv
Write-Host "`noutput_fail.csv:" -ForegroundColor Green
Get-Content .\output_fail.csv