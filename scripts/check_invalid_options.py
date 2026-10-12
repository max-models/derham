"""Check that invalid derham inputs fail with package errors.

Keep diagnostic text out of l3build snapshots: LaTeX versions format the
surrounding transcript differently. This check asserts the actual failures.
"""

from pathlib import Path
import os
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "invalid_dimension": (r"\[\derhamcomplex[dimension=0]\]", "Dimension must be"),
    "invalid_range": (r"\[\derhamcomplex[from=2,to=1]\]", "Degree range"),
    "invalid_vector_dimension": (
        r"\[\derhamcomplex[dimension=4,notation=vector]\]",
        "Vector notation",
    ),
    "invalid_list_length": (
        r"\[\derhamcomplex[dimension=2,custom-spaces={A,B}]\]",
        "Option 'custom-spaces'",
    ),
    "invalid_override_index": (
        r"\[\derhamcomplex[dimension=1,operator-2=Q]\]",
        "Index 2",
    ),
    "unknown_key": (r"\[\derhamcomplex[nonsense=true]\]", "Unknown option"),
    "duplicate_row": (
        r"\[\begin{derhamdiagram}[dimension=1]"
        r"\derhamrow[name=a]\derhamrow[name=a]"
        r"\end{derhamdiagram}\]",
        "Row 'a' is already defined",
    ),
    "missing_row": (
        r"\[\begin{derhamdiagram}[dimension=1]"
        r"\derhamrow[name=a]\derhamconnect[from=a,to=missing]"
        r"\end{derhamdiagram}\]",
        "Connection references unknown row",
    ),
    "invalid_connection_degree": (
        r"\[\begin{derhamdiagram}[dimension=1]"
        r"\derhamrow[name=a]\derhamrow[name=b]"
        r"\derhamconnect[from=a,to=b,degree=3]"
        r"\end{derhamdiagram}\]",
        "Connection degree 3",
    ),
    "incomplete_connection": (
        r"\[\begin{derhamdiagram}[dimension=1]"
        r"\derhamrow[name=a]\derhamrow[name=b]"
        r"\derhamconnect[from=a,to=b,from-degree=0]"
        r"\end{derhamdiagram}\]",
        "Set both from-degree and to-degree",
    ),
}


def main() -> None:
    environment = os.environ.copy()
    environment["TEXINPUTS"] = f"{ROOT}{os.pathsep}" + environment.get("TEXINPUTS", "")
    with tempfile.TemporaryDirectory(prefix="derham-invalid-") as directory:
        work = Path(directory)
        for name, (body, expected) in CASES.items():
            source = work / f"{name}.tex"
            source.write_text(
                "\\documentclass{article}\n\\usepackage{derham}\n"
                "\\begin{document}\n" + body + "\n\\end{document}\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    f"-output-directory={work}",
                    str(source),
                ],
                cwd=ROOT,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            transcript = result.stdout
            if result.returncode == 0 or f"Package derham Error: {expected}" not in transcript:
                raise AssertionError(f"{name} did not produce the expected error:\n{transcript[-1800:]}")
            print(f"{name}: expected derham error")


if __name__ == "__main__":
    main()
