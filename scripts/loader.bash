#!/bin/bash

PROJECT_ROOT="$(dirname $(dirname $(realpath $BASH_SOURCE[0])))"

rm ~/king-county-assessor.sqlite3
"$PROJECT_ROOT/.tox/py35/bin/create-sqlite-database"
sqlite3 -csv -header ~/king-county-assessor.sqlite3 \
        < "$PROJECT_ROOT/sql/get_unit_count_by_year_built.sql" \
        > "$PROJECT_ROOT/output/square_footage_by_year_built.csv"
