#!/bin/bash

PROJECT_ROOT="$(dirname $(dirname $(realpath $BASH_SOURCE[0])))"
GIS_ROOT=~/king-county-gis

function make_csv() {
    database=$1
    output_file=$2

    sql="${PROJECT_ROOT}/sql/populate/${output_file}.sql"
    output_file="${PROJECT_ROOT}/output/${output_file}.csv"
    echo "Running $sql in database $database and dumping to $output_file"
    spatialite -csv -header "$database" < "$sql" > "$output_file"
}

make_csv ~/king-county-gis/king-county-shapes.spatialite parcel_neighborhood

make_csv ~/king-county-assessor.sqlite3 seattle_yearly_unit_counts
make_csv ~/king-county-assessor.sqlite3 king_county_yearly_unit_counts

make_csv ~/king-county-gis/king-county-shapes.spatialite parcel_city

