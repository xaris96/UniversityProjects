# choices13k reproducible setup

This repository is configured to run with **Python 3.13.x**.
For reproducible results, use a clean virtual environment and the lock file.

## 1. Create environment and install dependencies

### Windows (PowerShell)
```powershell
.\setup_env.ps1
```

### macOS / Linux (bash)
```bash
chmod +x setup_env.sh
./setup_env.sh
```

## 2. Open the notebook

Open `choices13k_assignment.ipynb` and select kernel:

`choices13k (Python 3.13)`

## 3. Verify environment manually (optional)

### Windows
```powershell
.\.venv\Scripts\python verify_env.py
```

### macOS / Linux
```bash
source .venv/bin/activate
python verify_env.py
```

## Dependency files

- `requirements.txt`: core pinned packages (direct dependencies).
- `requirements.lock.txt`: full pinned set for stricter reproducibility.
