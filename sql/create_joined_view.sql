CREATE TABLE parcels_view AS
SELECT
  parcels_footage.major,
  parcels_footage.minor,
  parcels_footage.date_retrieved,
  
  appr_land_val,
  apr_imps_val,
  taxable_imps_val,
  taxable_land_val,

  current_zoning,
  square_footage,
  unit_count,
  source,
  year_built,
  district_name
  
FROM parcels_footage
LEFT JOIN parcels ON
  (
  parcels_footage.major = parcels.major AND
  parcels_footage.minor = parcels.minor AND
  parcels_footage.date_retrieved = parcels.date_retrieved
  )

LEFT JOIN parcels_appraisal ON
  (
  parcels_appraisal.major = parcels_footage.major AND
  parcels_appraisal.minor = parcels_footage.minor AND
  parcels_appraisal.date_retrieved = parcels_footage.date_retrieved
  )
;
