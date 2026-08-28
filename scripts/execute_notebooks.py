#!/usr/bin/env python3
"""Execute reproducibility notebooks with the current Python interpreter.

Uses ``sys.executable -m nbconvert`` so execution does not depend on a
``jupyter`` / ``jupyter-nbconvert`` binary from PATH (e.g. a global Anaconda
install). An ephemeral kernelspec is created that points at ``sys.executable``,
avoiding kernelspecs whose argv is a bare ``python`` resolved via PATH.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = (
    ROOT / "notebooks" / "reproducibility" / "01_scopus.ipynb",
    ROOT / "notebooks" / "reproducibility" / "02_web_of_science.ipynb",
    ROOT / "notebooks" / "reproducibility" / "03_selection.ipynb",
)
KERNEL_NAME = "re_te_lowresources_exec"


def _write_ephemeral_kernelspec(jupyter_path: Path) -> None:
    """Install a temporary kernelspec whose argv uses sys.executable."""
    kernel_dir = jupyter_path / "kernels" / KERNEL_NAME
    kernel_dir.mkdir(parents=True, exist_ok=True)
    spec = {
        "argv": [
            sys.executable,
            "-m",
            "ipykernel_launcher",
            "-f",
            "{connection_file}",
        ],
        "display_name": "re_te_lowresources (current interpreter)",
        "language": "python",
        "metadata": {"debugger": True},
    }
    (kernel_dir / "kernel.json").write_text(
        json.dumps(spec, indent=2) + "\n", encoding="utf-8"
    )


def _execute_notebook(notebook: Path, output_dir: Path, env: dict[str, str]) -> None:
    out_name = f"{notebook.stem}.executed.ipynb"
    cmd = [
        sys.executable,
        "-m",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        f"--output={out_name}",
        f"--output-dir={output_dir}",
        f"--ExecutePreprocessor.kernel_name={KERNEL_NAME}",
        "--ExecutePreprocessor.timeout=300",
        str(notebook),
    ]
    print(f"Executing: {notebook.relative_to(ROOT)}")
    print(f"  interpreter: {sys.executable}")
    print(f"  python: {sys.version.split()[0]}")
    proc = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        raise SystemExit(
            f"FAIL: notebook execution failed for {notebook.relative_to(ROOT)} "
            f"(exit {proc.returncode})"
        )
    print(f"  PASS: {notebook.name}")


def main() -> int:
    missing = [p for p in NOTEBOOKS if not p.is_file()]
    if missing:
        for path in missing:
            print(f"FAIL: missing notebook {path}", file=sys.stderr)
        return 1

    # Refuse accidental Anaconda routing of *this* process.
    if "/opt/anaconda3/" in sys.executable.replace("\\", "/"):
        print(
            "FAIL: current interpreter is under /opt/anaconda3; "
            "activate the project .venv and re-run.",
            file=sys.stderr,
        )
        return 1

    jupyter_data = Path(tempfile.mkdtemp(prefix="re_te_jupyter_path_"))
    output_dir = Path(tempfile.mkdtemp(prefix="re_te_nb_out_"))
    try:
        _write_ephemeral_kernelspec(jupyter_data)
        env = os.environ.copy()
        # Prefer our ephemeral kernelspec directory.
        existing = env.get("JUPYTER_PATH", "")
        env["JUPYTER_PATH"] = (
            str(jupyter_data)
            if not existing
            else os.pathsep.join([str(jupyter_data), existing])
        )

        for notebook in NOTEBOOKS:
            _execute_notebook(notebook, output_dir, env)

        print()
        print(f"Interpreter: {sys.executable}")
        print(f"Outputs (temporary): {output_dir}")
        print("PASS")
        return 0
    finally:
        shutil.rmtree(jupyter_data, ignore_errors=True)
        # Keep executed copies only for the process lifetime; remove temp outputs.
        shutil.rmtree(output_dir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
