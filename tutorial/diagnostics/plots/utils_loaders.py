import numpy as np


def to_numeric_safe(arr):
    """
    Convert any ObsValue/hofx/OMB/OMA array to float64.
    Replace masked, object, or invalid entries with NaN.
    """
    if arr is None:
        return None

    if hasattr(arr, "filled"):
        arr = arr.filled(np.nan)

    arr = np.array(arr)

    if arr.dtype == object:
        out = np.empty(arr.shape, dtype="float64")
        for idx, v in np.ndenumerate(arr):
            try:
                out[idx] = float(v)
            except Exception:
                out[idx] = np.nan
        return out

    return arr.astype("float64")


def load_qc_universal(f, varname):
    """
    Try multiple QC groups. If group exists but variable missing → all-valid.
    If no QC groups exist → all-valid.
    """
    qc_groups = [
        "EffectiveQC2",
        "EffectiveQC1",
        "EffectiveQC0",
        "EffectiveQC",
        "ObsDiag",
        "QualityControl",
        "FortranQC",
    ]

    for grp in qc_groups:
        if grp in f.groups:
            g = f.groups[grp]
            if varname in g.variables:
                return to_numeric_safe(g.variables[varname][:]).astype("int32")

            alt = f"{varname}@{grp}"
            if alt in f.variables:
                return to_numeric_safe(f[alt][:]).astype("int32")

            nloc = f.dimensions["Location"].size
            return np.zeros(nloc, dtype="int32")

    nloc = f.dimensions["Location"].size
    return np.zeros(nloc, dtype="int32")


def load_obsvalue(f, varname):
    if "ObsValue" in f.groups and varname in f.groups["ObsValue"].variables:
        return to_numeric_safe(f.groups["ObsValue"].variables[varname][:])
    return None


def load_hofx(f, varname):
    if "hofx0" in f.groups and varname in f.groups["hofx0"].variables:
        return to_numeric_safe(f.groups["hofx0"].variables[varname][:])
    return None


def load_omb(f, varname):
    """
    Universal OMB loader.

    Priority:
      1. ombg/<varname> (ATMS, GNSSRO, SATWND, SCATWND, CONVENTIONAL_PS)
      2. innov1/<varname> (some IODA formats)
      3. DerivedMetaData/Innovation (fallback, e.g. ATMS)
    """
    if "ombg" in f.groups and varname in f.groups["ombg"].variables:
        return to_numeric_safe(f.groups["ombg"].variables[varname][:])

    if "innov1" in f.groups and varname in f.groups["innov1"].variables:
        return to_numeric_safe(f.groups["innov1"].variables[varname][:])

    if "DerivedMetaData" in f.groups and "Innovation" in f.groups["DerivedMetaData"].variables:
        return to_numeric_safe(f.groups["DerivedMetaData"].variables["Innovation"][:])

    return None


def load_oma_explicit(f, varname):
    """
    Universal OMA loader.

    Priority:
      1. oman/<varname> (ATMS, GNSSRO, SATWND, SCATWND, CONVENTIONAL_PS)
      2. ObsValue - hofx (fallback)
    """
    if "oman" in f.groups and varname in f.groups["oman"].variables:
        return to_numeric_safe(f.groups["oman"].variables[varname][:])

    obs = load_obsvalue(f, varname)
    hofx = load_hofx(f, varname)
    if obs is None or hofx is None:
        return None

    return to_numeric_safe(obs - hofx)
