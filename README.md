These are some scripts I threw together to study the rate of housing construction in Seattle. They rely on the [King County Assessor's data.](http://info.kingcounty.gov/assessor/DataDownload/default.aspx), and assume that you have downloaded the data files and extracted them to your home directory at `~/king-county-assessor/<date>/<files>`. E.g. I have two extracts I downloaded at the end of 2016 and more recently at the end of 2017, so they are at `~/king-county-assessor/2016-12-30/EXTR_ResBldg.csv` and `~/king-county-assessor/2018-01-10/EXTR_ResBldg.csv`.

To run it, run tox to create a virtualenv with the project, then run create-sqlite-database, e.g.

```
tox
.tox/py35/bin/create-sqlite-database
```

This will create a sqlite3 database at `~/king-county-assessor.sqlite3`

You can then play around with the data:

```
sqlite3 ~/king-county-assessor.sqlite3 
```

I have an attached script at `sql/get_unit_count_by_year_built.sql`, but it's hardcoded to generate data for my `2018-01-10` dump so you'll have to edit it unless you have my 2018-01-10 dataset, but then you can do something like this:

```
sqlite3 -csv -header ~/king-county-assessor.sqlite3 < sql/get_unit_count_by_year_built.sql > output/square_footage_by_year_built.csv
```

[This CSV has the output for that query.](output/square_footage_by_year_built.csv)

# Assessor Files

This is my understanding of the files, gleaned from conversations with other people but mostly from analysis of the data files and (very sparse) documentation provided by the Assessor's office.

All files have the "Major","Minor" fields which together are the unique key for a parcel.

## Building type files
These files appear to be subsets of the parcels which only have a specific type of building. Detached single family homes are in the `EXTR_ResBldg` file. `EXTR_CondoComplex` and `EXTR_AptComplex` seem to be what they say (apartment and condominium complexes.)

* `EXTR_ResBldg.csv`
** The fields I am interested in this file are `YrBuilt`, `SqFtTotLiving`
* `EXTR_CondoComplex` / `EXTR_AptComplex`
** For my purposes these files are more or less the same. The keys I look at are `YrBuilt`, `AvgUnitSize`, `NbrUnits`
* `EXTR_Parcel.csv`
** This file has the most 
* `EXTR_RPAcct_NoName.csv` seems to contain the actual appraisals.
** This file contains `TaxableLandVal`,`TaxableImpsVal`,`ApprLandVal`,`ApprImpsVal`


# Source Material

* [King County Assessor data](http://info.kingcounty.gov/assessor/DataDownload/default.aspx)
* [King County Neighborhood Maps (Shapefile)](https://gis-kingcounty.opendata.arcgis.com/datasets/metro-neighborhoods-in-king-county--neighborhood-area?geometry=-122.506%2C47.576%2C-122.042%2C47.657)
* [King County Tax Parcels (Shapefile)](https://gis-kingcounty.opendata.arcgis.com/datasets/king-county-parcels--parcel-area?geometry=-122.315%2C47.603%2C-122.286%2C47.608)
* [King County Incorporated Areas (Cities/Municipalities) (Shapefiles)](https://gis-kingcounty.opendata.arcgis.com/datasets/incorporated-areas-of-king-county--city-area?geometry=-123.731%2C47.129%2C-120.02%2C47.779)
