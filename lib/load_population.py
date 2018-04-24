import os
import csv
import glob
from pathlib import Path
import sqlite3
from collections import defaultdict


def main():
    PROJECT_ROOT = Path(__file__).parent.parent
    DATABASE = str(Path(Path.home(), 'king-county-assessor.sqlite3'))

    with sqlite3.connect(DATABASE) as connection:
        connection.execute('DROP TABLE IF EXISTS population;')

        create_parcels_footage = '''
          CREATE TABLE population (
            year INTEGER,
            king_county INTEGER,
            seattle INTEGER
        );
        '''
        connection.execute(create_parcels_footage)

        file_path = os.path.join(str(PROJECT_ROOT), 'data', 'population.csv')
        with open(file_path) as f:
            rows = csv.DictReader(f)
            print('loading csv: ' + file_path + '\n')

            raw_data = {
                int(row['year']): row
                for row in rows
            }

            interpolated_data = defaultdict(dict)
            interpolated_data.update(raw_data)

            for area in 'seattle', 'king_county':
                for base_year in range(1900, 2000, 10):
                    print('interpolating {}'.format(base_year))
                    next_year = base_year + 10
                    base_pop = int(raw_data[base_year][area])
                    step = (int(raw_data[next_year][area]) - base_pop) / 10

                    for year in range(base_year + 1, next_year):
                        base_pop += step
                        interpolated_data[year]['year'] = year
                        interpolated_data[year][area] = base_pop

            connection.executemany(
                '''
                INSERT INTO population
                  (year, seattle, king_county)
                VALUES
                  (:year,:seattle,:king_county)
                ''',
                interpolated_data.values()
            )
