"""Compile a derham math expression with tikzfigure for the executable guide."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from IPython.display import Image, display
from tikzfigure import TikzFigure

REPO = Path(__file__).resolve().parents[2]


class DerhamFigure(TikzFigure):
    """A tikzfigure export whose body is a derham math object.

    tikzfigure normally wraps its body in ``tikzpicture``. derham already emits
    ``tikzcd``, so its standalone document needs the math object directly.
    Compilation and raster export still use tikzfigure's methods.
    """

    def __init__(self, expression: str):
        super().__init__()
        self.expression = expression

    def generate_standalone(self, **_kwargs) -> str:
        return (
            r"\documentclass[border=12pt]{standalone}" "\n"
            r"\usepackage{derham}" "\n"
            r"\begin{document}" "\n"
            r"\(\displaystyle " + self.expression + r"\)" "\n"
            r"\end{document}" "\n"
        )


def show_derham(expression: str, *, dpi: int = 180) -> None:
    """Compile a package command and display its PNG output in a notebook."""
    # pdflatex runs inside tikzfigure's temporary directory.
    os.environ["TEXINPUTS"] = str(REPO) + os.pathsep + os.environ.get("TEXINPUTS", "")
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "diagram.png"
        DerhamFigure(expression).savefig(output, dpi=dpi, transparent=False)
        display(Image(data=output.read_bytes()))
