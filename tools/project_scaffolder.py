from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent


@dataclass
class ProjectSpec:
    name: str
    project_type: str  # "fastapi_app" | "cli_tool"
    destination: Path

    @property
    def root(self) -> Path:
        return self.destination / self.name


def scaffold_project(spec: ProjectSpec) -> list[str]:
    """Create a small, opinionated project skeleton.

    Returns a list of created paths (as strings).
    """
    created: list[str] = []

    spec.root.mkdir(parents=True, exist_ok=True)

    if spec.project_type == "fastapi_app":
        created.extend(_scaffold_fastapi_app(spec))
    elif spec.project_type == "cli_tool":
        created.extend(_scaffold_cli_tool(spec))
    else:
        raise ValueError(f"Tipo progetto non supportato: {spec.project_type}")

    return created


def _scaffold_fastapi_app(spec: ProjectSpec) -> list[str]:
    created: list[str] = []
    root = spec.root

    (root / "app").mkdir(parents=True, exist_ok=True)

    main_py = root / "app" / "main.py"
    main_py.write_text(
        dedent(
            f"""\
            from fastapi import FastAPI


            app = FastAPI(title="{spec.name}")


            @app.get("/")
            async def root_endpoint() -> dict[str, str]:
                return {{"message": "API {spec.name} attiva"}}
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    created.append(str(main_py))

    req = root / "requirements.txt"
    req.write_text("fastapi\nuvicorn[standard]\n", encoding="utf-8")
    created.append(str(req))

    readme = root / "README.md"
    readme.write_text(
        dedent(
            f"""\
            # {spec.name}

            Mini API FastAPI generata da Super Agent.

            ## Avvio

            ```pwsh
            cd {spec.name}
            python -m venv .venv
            .venv\\Scripts\\python.exe -m pip install -r requirements.txt
            .venv\\Scripts\\uvicorn.exe app.main:app --reload --host 0.0.0.0 --port 8000
            ```
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    created.append(str(readme))

    return created


def _scaffold_cli_tool(spec: ProjectSpec) -> list[str]:
    created: list[str] = []
    root = spec.root

    src = root / spec.name.replace("-", "_")
    src.mkdir(parents=True, exist_ok=True)

    main_py = src / "__main__.py"
    main_py.write_text(
        dedent(
            f"""\
            import argparse


            def build_parser() -> argparse.ArgumentParser:
                parser = argparse.ArgumentParser(prog="{spec.name}")
                parser.add_argument("name", nargs="?", default="mondo", help="Chi salutare")
                return parser


            def main(argv: list[str] | None = None) -> int:
                parser = build_parser()
                args = parser.parse_args(argv)
                print(f"Ciao, {{args.name}}! Questo è {spec.name}.")
                return 0


            if __name__ == "__main__":  # pragma: no cover
                raise SystemExit(main())
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    created.append(str(main_py))

    req = root / "requirements.txt"
    req.write_text("", encoding="utf-8")
    created.append(str(req))

    readme = root / "README.md"
    readme.write_text(
        dedent(
            f"""\
            # {spec.name}

            Utility CLI Python generata da Super Agent.

            ## Avvio

            ```pwsh
            cd {spec.name}
            python -m venv .venv
            .venv\\Scripts\\python.exe -m pip install -r requirements.txt
            .venv\\Scripts\\python.exe -m {spec.name.replace('-', '_')} --help
            ```
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    created.append(str(readme))

    return created
