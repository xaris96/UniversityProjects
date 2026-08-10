$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python launcher 'py' was not found. Install Python 3.13 first."
}

py -3.13 -m venv .venv
$python = Join-Path $root ".venv\Scripts\python.exe"

& $python -m pip install --upgrade pip
& $python -m pip install -r (Join-Path $root "requirements.lock.txt")
& $python -m ipykernel install --user --name choices13k-py313 --display-name "choices13k (Python 3.13)"
& $python (Join-Path $root "verify_env.py")

Write-Output "Setup complete. Select kernel: choices13k (Python 3.13)"
