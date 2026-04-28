# plots/__init__.py

# Spectra diagnostics (your existing module)
from .spectra_plots import SpectraPlotter

# New unified observation diagnostics orchestrator
from .obs_diag_plotter import ObsDiagPlotter

__all__ = [
    "SpectraPlotter",
    "ObsDiagPlotter",
]
