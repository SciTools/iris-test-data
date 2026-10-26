# Zarr sample stores

Published Zarr stores, cut down, for testing Iris's native Zarr reader and
writer. Each one is third-party data redistributed under its own licence, not
under the Open Government Licence the repository README offers for Met Office
data.

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
