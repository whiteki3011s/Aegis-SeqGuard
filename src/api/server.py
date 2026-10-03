from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from src.api.routes import router

app = FastAPI(
    title="AI Password Anti-Breaching System",
    description="Real-time authentication entry sequence anomaly detection and automated security lockout microservice.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root_dashboard():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return RedirectResponse(url="/docs")


app.include_router(router)
