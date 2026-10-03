import sys
from pathlib import Path

# Ensure project root directory is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn
from src.api.server import app

def main():
    print("Starting AI Password Anti-Breaching System API Server on http://127.0.0.1:8000 ...")
    uvicorn.run("src.api.server:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()

