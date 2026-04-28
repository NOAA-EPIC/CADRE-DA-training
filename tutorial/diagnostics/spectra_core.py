# spectra_core.py

import xarray as xr
import numpy as np
from scipy.interpolate import griddata


class SpectraCore:
    """
    Core FV3-JEDI diagnostics engine:
      - Tile loading
      - Grid loading
      - Cubed-sphere → lat/lon regridding
      - Isotropic spectra
      - Variance profile
      - 2D spectral ratio
    """

    def __init__(self, varname="T_inc", grid_prefix="./C96_grid.tile", suffix=".nc"):
        self.varname = varname
        self.grid_prefix = grid_prefix
        self.suffix = suffix
        self.nlevels = None
        self.k = None

    # ----------------------------------------------------------------------
    # Load FV3 tile
    # ----------------------------------------------------------------------
    def load_tile(self, prefix, tile, level):
        ds = xr.open_dataset(f"{prefix}{tile}{self.suffix}", engine="netcdf4")
        return ds[self.varname].isel(Time=0, zaxis_1=level).values

    # ----------------------------------------------------------------------
    # Load FV3 grid and convert corner → center
    # ----------------------------------------------------------------------
    def load_grid(self, tile):
        grid = xr.open_dataset(f"{self.grid_prefix}{tile}{self.suffix}", engine="netcdf4")
        lon = grid["x"].values
        lat = grid["y"].values

        lon_c = 0.25 * (lon[0:-1:2, 0:-1:2] +
                        lon[1::2,   0:-1:2] +
                        lon[0:-1:2, 1::2] +
                        lon[1::2,   1::2])

        lat_c = 0.25 * (lat[0:-1:2, 0:-1:2] +
                        lat[1::2,   0:-1:2] +
                        lat[0:-1:2, 1::2] +
                        lat[1::2,   1::2])

        lon_c = (lon_c + 180) % 360 - 180
        return lon_c, lat_c

    # ----------------------------------------------------------------------
    # Build global field for a single level
    # ----------------------------------------------------------------------
    def build_global(self, prefix, level):
        fields, lons, lats = [], [], []

        for t in range(1, 7):
            fields.append(self.load_tile(prefix, t, level))
            lon_c, lat_c = self.load_grid(t)
            lons.append(l_c := lon_c)
            lats.append(lat_c)

        field_global = np.concatenate([f.flatten() for f in fields])
        lon_global   = np.concatenate([g.flatten() for g in lons])
        lat_global   = np.concatenate([g.flatten() for g in lats])

        lon_new = np.linspace(-180, 180, 360)
        lat_new = np.linspace(-90, 90, 181)
        Lon, Lat = np.meshgrid(lon_new, lat_new)

        field_interp = griddata(
            points=(lon_global, lat_global),
            values=field_global,
            xi=(Lon, Lat),
            method="nearest"
        )

        return Lon, Lat, field_interp

    # ----------------------------------------------------------------------
    # Build global fields for all levels
    # ----------------------------------------------------------------------
    def build_global_all_levels(self, prefix, nlevels):
        Lon, Lat = None, None
        fields = []

        for lev in range(nlevels):
            Lon, Lat, field = self.build_global(prefix, lev)
            fields.append(field)

        return Lon, Lat, np.array(fields)

    # ----------------------------------------------------------------------
    # Isotropic spectrum
    # ----------------------------------------------------------------------
    def isotropic_spectrum(self, field):
        ny, nx = field.shape

        F = np.fft.fftshift(np.fft.fft2(field))
        P = np.abs(F)**2

        ky = np.fft.fftshift(np.fft.fftfreq(ny))
        kx = np.fft.fftshift(np.fft.fftfreq(nx))
        KX, KY = np.meshgrid(kx, ky)
        K = np.sqrt(KX**2 + KY**2)

        kmax = int(np.sqrt((nx/2)**2 + (ny/2)**2))
        spectrum = np.zeros(kmax)
        counts = np.zeros(kmax)

        for i in range(ny):
            for j in range(nx):
                k = int(K[i, j] * kmax)
                if k < kmax:
                    spectrum[k] += P[i, j]
                    counts[k] += 1

        return spectrum / np.maximum(counts, 1)

    # ----------------------------------------------------------------------
    # Load CTRL and EXP fields (full vertical)
    # ----------------------------------------------------------------------
    def load_fields(self, ctrl_prefix, exp_prefix, nlevels=127):
        self.Lon, self.Lat, self.CTRL_3D = self.build_global_all_levels(ctrl_prefix, nlevels)
        _,      _,      self.EXP_3D  = self.build_global_all_levels(exp_prefix,  nlevels)

        self.nlevels = nlevels

        self.spec_ctrl_all = []
        self.spec_exp_all  = []

        for lev in range(nlevels):
            sc = self.isotropic_spectrum(self.CTRL_3D[lev])
            se = self.isotropic_spectrum(self.EXP_3D[lev])
            self.spec_ctrl_all.append(sc)
            self.spec_exp_all.append(se)

        self.spec_ctrl_all = np.array(self.spec_ctrl_all)
        self.spec_exp_all  = np.array(self.spec_exp_all)

        self.spec_ratio_all = self.spec_exp_all / np.maximum(self.spec_ctrl_all, 1e-12)
        self.k = np.arange(self.spec_ctrl_all.shape[1])

    # ----------------------------------------------------------------------
    # Variance profile
    # ----------------------------------------------------------------------
    def variance_profile(self):
        var_ctrl = self.spec_ctrl_all.sum(axis=1)
        var_exp  = self.spec_exp_all.sum(axis=1)
        return var_exp / np.maximum(var_ctrl, 1e-12)

    # ----------------------------------------------------------------------
    # 2D spectral ratio
    # ----------------------------------------------------------------------
    def spectral_ratio_2d(self):
        return self.spec_ratio_all
