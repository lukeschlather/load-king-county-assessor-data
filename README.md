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
