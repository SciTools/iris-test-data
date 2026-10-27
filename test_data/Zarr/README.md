# Zarr sample stores

Zarr stores for testing Iris's native Zarr reader and writer. Some are
published data cut down, and those are third-party, redistributed under their
own licence rather than under the Open Government Licence the repository
README offers for Met Office data. Each section below says which it is.

A Zarr store is a directory, not a file. Point Iris at the directory.

## `gfs_forecast_sample.zarr`

A subset of the NOAA GFS forecast archive published by dynamical.org, in Zarr
version 3.

**Licence:** CC BY 4.0. DOI 10.5281/zenodo.18777399.

**Attribution**, as the store's own root `attribution` attribute gives it:

> NOAA NWS NCEP GFS data processed by dynamical.org from NOAA Open Data
> Dissemination archives.

The subset keeps every source attribute verbatim, so `license` and
`attribution` travel in the data itself. This file is what makes them visible
to someone reading the repository.

**What the subset is.** 1.4 MB over 35 files. Two forecast initialisations,
eight lead times, 120 x 120 points. Four data variables — `temperature_2m`,
`wind_u_10m`, `wind_v_10m` and `precipitation_surface` — with the
`init_time`, `lead_time`, `latitude`, `longitude` and `valid_time` coordinate
variables they reference.

**What was kept deliberately**, because it is what the fixture exists to
exercise:

- The **sharding codec**. The data arrays are sharded `(1, 4, 120, 120)` over
  inner chunks `(1, 2, 40, 40)`, which is what exercises the rule that a
  reader fetches inner chunks while a writer must align to whole shards.
- The scalar **`spatial_ref`** variable, carrying `crs_wkt` and the rest of a
  CF grid mapping. Note that the data variables name it in `coordinates` and
  carry no `grid_mapping` attribute, so it is not referenced the way CF asks
  for a grid mapping to be referenced.
- The two-dimensional **`valid_time`** auxiliary coordinate, which spans
  `init_time` and `lead_time` together.
- The **base64 `_FillValue`** encoding on every floating variable. This is
  what released xarray writes for a float, so a reader that cannot read it
  cannot read the wider Zarr ecosystem's output.

**Provenance.** `https://data.dynamical.org/noaa/gfs/forecast/`, dataset
`noaa-gfs-forecast` version 0.2.7. That endpoint was documented as closing on
30 September 2026, which is why the subset was cut ahead of the work that
needed it.

## `unicode_coords_v2.zarr` and `unicode_coords_v3.zarr`

The same tiny dataset in Zarr version 2 and version 3, holding fixed-length
unicode coordinate arrays. 80 KB and 84 KB.

**Licence:** these are ours. Synthetic data, no third party involved, so the
repository's Open Government Licence applies as it does to everything outside
`gfs_forecast_sample.zarr`.

**What they are for.** A `<U` array is not strictly Zarr-supported — see
[SciTools/iris#6961](https://github.com/SciTools/iris/issues/6961) — and real
stores contain them anyway, so Iris needs a defined answer rather than an
accident. A test that writes such an array and reads it back cannot pin that:
if the writing library ever changes its encoding, both halves move together
and the test still passes, while a file written years earlier stops loading.
These stores are the frozen half of that pair.

**Do not regenerate them.** Their value is that the bytes do not move.
`make_unicode_coords.py` is here to record how they were made, not to replace
them; re-running it against a newer zarr-python would pin only what that
version does today. As written, with zarr-python 3.4.1, the version 2 store
records `"dtype": "<U7"` and the version 3 store records
`fixed_length_utf32` with `length_bytes: 28`.

**Shape.** One data variable, `viewing_incidence_angle`, over `band` (13),
`detector` (5) and `angle` (2), with a string coordinate on each dimension:
`<U3` for band and detector, `<U7` for angle. Those shapes and dtypes follow
the ESA EOPF Sentinel-2 products' `conditions/geometry` group, which is where
the question came from. The values are invented.
