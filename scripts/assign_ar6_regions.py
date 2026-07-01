from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import regionmask


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "Paper1"
REGISTRY = ROOT / "Data" / "harmonized" / "station_registry" / "station_registry_v1.csv"
OUT = PAPER / "stations_ar6.csv"
MAP = PAPER / "stations_ar6_map.png"


def main() -> None:
    stations = pd.read_csv(REGISTRY, dtype=str)
    for col in ["latitude", "longitude", "elevation_m"]:
        stations[col] = pd.to_numeric(stations[col], errors="coerce")

    valid_coord = (
        stations["latitude"].between(-90, 90)
        & stations["longitude"].between(-180, 180)
        & stations["latitude"].notna()
        & stations["longitude"].notna()
    )

    gdf = gpd.GeoDataFrame(
        stations.loc[valid_coord].copy(),
        geometry=gpd.points_from_xy(
            stations.loc[valid_coord, "longitude"],
            stations.loc[valid_coord, "latitude"],
        ),
        crs="EPSG:4326",
    )

    ar6 = regionmask.defined_regions.ar6.land
    ar6_gdf = ar6.to_geodataframe()[["abbrevs", "names", "geometry"]].rename(
        columns={"abbrevs": "ar6_region", "names": "ar6_name"}
    )
    ar6_gdf = gpd.GeoDataFrame(ar6_gdf, geometry="geometry", crs="EPSG:4326")

    joined = gpd.sjoin(gdf, ar6_gdf, how="left", predicate="within")
    joined = pd.DataFrame(joined.drop(columns=["geometry", "index_right"], errors="ignore"))

    out = stations[
        [
            "source_id",
            "source_station_id",
            "station_name",
            "country_iso3",
            "latitude",
            "longitude",
            "elevation_m",
            "position_kind",
            "wmo_id",
            "candidate_duplicate_key",
        ]
    ].copy()
    out = out.merge(
        joined[["source_id", "source_station_id", "ar6_region", "ar6_name"]],
        on=["source_id", "source_station_id"],
        how="left",
    )

    out["exclusion_reason"] = ""
    out.loc[~valid_coord.values, "exclusion_reason"] = "invalid_or_missing_coordinates"
    out.loc[
        valid_coord.values & out["ar6_region"].isna(), "exclusion_reason"
    ] = "not_in_ar6_land_region_or_boundary"
    out.loc[out["ar6_region"].notna(), "exclusion_reason"] = ""
    out["station_uid"] = out["source_id"] + "::" + out["source_station_id"].astype(str)

    cols = [
        "station_uid",
        "source_id",
        "source_station_id",
        "station_name",
        "country_iso3",
        "latitude",
        "longitude",
        "elevation_m",
        "position_kind",
        "wmo_id",
        "candidate_duplicate_key",
        "ar6_region",
        "ar6_name",
        "exclusion_reason",
    ]
    out[cols].to_csv(OUT, index=False)

    fig, ax = plt.subplots(figsize=(13, 7))
    ar6_gdf.boundary.plot(ax=ax, linewidth=0.4, color="0.4")
    sample = out[out["ar6_region"].notna()].copy()
    if len(sample) > 40000:
        sample = sample.sample(40000, random_state=7)
    ax.scatter(
        sample["longitude"],
        sample["latitude"],
        s=1,
        c=pd.factorize(sample["ar6_region"])[0],
        cmap="tab20",
        alpha=0.7,
        linewidths=0,
    )
    ax.set_title("Station assignment to IPCC AR6 land regions")
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")
    ax.set_xlim(-25, 45)
    ax.set_ylim(25, 75)
    fig.tight_layout()
    fig.savefig(MAP, dpi=180)

    summary = out["ar6_region"].fillna("EXCLUDED").value_counts().reset_index()
    summary.columns = ["ar6_region", "n_stations"]
    summary.to_csv(PAPER / "stations_ar6_summary.csv", index=False)

    print(f"wrote {OUT}")
    print(f"wrote {MAP}")
    print(ar6)
    print(summary.head(20).to_string(index=False))


if __name__ == "__main__":
    main()

