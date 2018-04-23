WITH city AS
(
SELECT *
FROM Incorporated_Areas_of_King_County__city_area
)

SELECT major,minor,pin,cityname,city.JURIS
FROM King_County_Parcels__parcel_area,city
WHERE st_contains(city.Geometry, King_County_Parcels__parcel_area.Geometry);
