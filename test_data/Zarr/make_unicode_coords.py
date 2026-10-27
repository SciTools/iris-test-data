"""Write the Zarr stores that pin Iris's reading of fixed-length unicode.

WARNING: do not re-run this to "refresh" the stored fixtures. Their value is
that they are frozen. They record how one version of zarr-python encoded a
`<U` array, so that Iris can be held to reading that encoding years later. A
regenerated store pins only whatever the installed zarr-python does today,
which the unit tests in `lib/iris/tests/unit/fileformats/zarr/` already cover
by writing and reading in the same breath. This script is here to say where
the bytes came from, not to replace them.

The shapes and dtypes are those the ESA EOPF Sentinel-2 products carry under
`conditions/geometry` - `<U7` for the angle names, `<U3` for the band and
detector labels. The values are invented, so nothing here is third-party
data. See https://github.com/SciTools/iris/issues/6961 for why `<U` dtypes
are worth pinning at all.

Written with zarr-python 3.4.1.
"""

from pathlib import Path
import sys

import numpy as np
import zarr

#: `<U7` on the real products: "azimuth" is the longest value.
ANGLES = np.array(["zenith", "azimuth"], dtype="<U7")
#: `<U3` on the real products.
BANDS = np.array([f"b{n:02d}" for n in range(1, 14)], dtype="<U3")
DETECTORS = np.array([f"d{n:02d}" for n in range(1, 6)], dtype="<U3")

DIMENSIONS = ("band", "detector", "angle")
SHAPE = (BANDS.size, DETECTORS.size, ANGLES.size)


def write_store(path: Path, zarr_format: int) -> None:
    """Write one store, recording dimension names the way its version does."""
    root = zarr.open_group(store=path, mode="w", zarr_format=zarr_format)
    root.attrs["Conventions"] = "CF-1.12"
    root.attrs["comment"] = (
        "Synthetic. Shapes and dtypes follow the ESA EOPF Sentinel-2 "
        "conditions/geometry group; the values are invented."
    )

    def make(name, values, dimensions, attributes=None):
        extra = {}
        if zarr_format == 3:
            extra["dimension_names"] = dimensions
        array = root.create_array(
            name, shape=values.shape, dtype=values.dtype, **extra
        )
        array[...] = values
        if zarr_format == 2:
            # zarr-python will not write version 2 dimension names itself.
            array.attrs["_ARRAY_DIMENSIONS"] = list(dimensions)
        for key, value in (attributes or {}).items():
            array.attrs[key] = value
        return array

    make("angle", ANGLES, ("angle",), {"long_name": "Angle name"})
    make("band", BANDS, ("band",), {"long_name": "Spectral band"})
    make("detector", DETECTORS, ("detector",), {"long_name": "Detector"})

    values = np.arange(np.prod(SHAPE), dtype="f4").reshape(SHAPE) / 10.0
    make(
        "viewing_incidence_angle",
        values,
        DIMENSIONS,
        {
            "long_name": "Viewing incidence angle",
            "units": "degrees",
            # Naming the three string arrays here is what attaches them to
            #  the cube as coordinates rather than loading them as cubes of
            #  their own, which is the shape worth pinning.
            "coordinates": "angle band detector",
            # Declared so that a version 2 read does not fall back to the
            #  storage fill value, and warn about doing so.
            "_FillValue": -999.0,
        },
    )

    zarr.consolidate_metadata(path)


if __name__ == "__main__":
    destination = Path(sys.argv[1])
    for zarr_format in (2, 3):
        store = destination / f"unicode_coords_v{zarr_format}.zarr"
        write_store(store, zarr_format)
        print(f"wrote {store}")
