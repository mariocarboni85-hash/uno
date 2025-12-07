from __future__ import annotations

from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from run_super_agent import main as super_agent_main


app = FastAPI(title="Super Agent API", version="0.1.0")


class AnalyzeRequest(BaseModel):
    path: str
    mode: str = "analizza"  # "analizza" oppure "security"


class AnalyzeResponse(BaseModel):
    path: str
    mode: str
    exit_code: int
    output: str


class StatusResponse(BaseModel):
    status: str
    detail: str = "Super Agent API attiva"


class ReportResponse(BaseModel):
    exit_code: int
    output: str


class LLMAssistRequest(BaseModel):
    path: str
    instruction: str = "Suggerisci miglioramenti e potenziali problemi in questo codice."


class LLMAssistResponse(BaseModel):
    path: str
    instruction: str
    output: str


class CreateProjectRequest(BaseModel):
    name: str
    project_type: str  # "fastapi_app" | "cli_tool"
    destination: str


class CreateProjectResponse(BaseModel):
    name: str
    project_type: str
    destination: str
    created_paths: list[str]


def _run_super_agent(args: List[str]) -> tuple[int, str]:
    import io
    from contextlib import redirect_stdout, redirect_stderr

    buf = io.StringIO()
    exit_code = 0
    try:
        with redirect_stdout(buf), redirect_stderr(buf):
            super_agent_main(args)
    except SystemExit as exc:  # type: ignore[assignment]
        exit_code = int(exc.code or 0)
    except Exception as exc:  # pragma: no cover
        exit_code = 1
        buf.write(f"\n[EXCEPTION] {exc}\n")
    return exit_code, buf.getvalue()


@app.get("/status", response_model=StatusResponse)
def get_status() -> StatusResponse:
    return StatusResponse(status="ok")


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_code(req: AnalyzeRequest) -> AnalyzeResponse:
    path = Path(req.path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="File non trovato")

    if req.mode not in {"analizza", "security"}:
        raise HTTPException(status_code=400, detail="mode deve essere 'analizza' o 'security'")

    args = [req.mode, "--file", str(path)]
    exit_code, output = _run_super_agent(args)
    return AnalyzeResponse(path=str(path), mode=req.mode, exit_code=exit_code, output=output)


@app.get("/report", response_model=ReportResponse)
def get_report() -> ReportResponse:
    args = ["report"]
    exit_code, output = _run_super_agent(args)
    return ReportResponse(exit_code=exit_code, output=output)


@app.post("/llm_assist", response_model=LLMAssistResponse)
def llm_assist(req: LLMAssistRequest) -> LLMAssistResponse:
    from tools.local_llm_client import get_default_client

    path = Path(req.path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="File non trovato")

    code = path.read_text(encoding="utf-8", errors="replace")
    prompt = (
        f"{req.instruction}\n\n"
        "Rispondi in italiano, in modo conciso.\n\n"
        "=== CODICE INIZIO ===\n"
        f"{code}\n"
        "=== CODICE FINE ===\n"
    )

    client = get_default_client()
    try:
        resp = client.generate(prompt)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Errore chiamando il modello locale: {exc}") from exc

    return LLMAssistResponse(path=str(path), instruction=req.instruction, output=resp.text.strip())


@app.post("/create_project", response_model=CreateProjectResponse)
def create_project(req: CreateProjectRequest) -> CreateProjectResponse:
    from tools.project_scaffolder import ProjectSpec, scaffold_project

    destination = Path(req.destination).expanduser().resolve()
    spec = ProjectSpec(
        name=req.name,
        project_type=req.project_type,
        destination=destination,
    )

    try:
        created = scaffold_project(spec)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return CreateProjectResponse(
        name=req.name,
        project_type=req.project_type,
        destination=str(destination),
        created_paths=created,
    )
