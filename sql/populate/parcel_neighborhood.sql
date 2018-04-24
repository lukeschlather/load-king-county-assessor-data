WITH neighborhoods AS
(
SELECT *
FROM Metro_Neighborhoods_in_King_County__neighborhood_area
)

SELECT
  major,
  minor,
  pin,
  NEIGHBORHO as neighborhood,
  NEIGH_NUM as neighborhood_number
FROM King_County_Parcels__parcel_area, neighborhoods
WHERE st_contains(neighborhoods.Geometry, King_County_Parcels__parcel_area.Geometry);
