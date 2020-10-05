import sqlalchemy as db
from sqlalchemy import desc, func
try:
    from .config import *
except:
    from config import *

import datetime

import pandas as pd

class ImportMovieMetata(object):

    @staticmethod
    def import_data(data_file):
        table_name = 'movie_metadata'
        db_engine, connection = get_static_connection()
        df = pd.read_csv(data_file)
        df.columns = [c.lower().replace(" ","_") for c in df.columns]
        df.to_sql(table_name, db_engine)
        connection.close()
        db_engine.dispose()

if __name__ == "__main__":
    data_file = "../../data/themoviesdataset/movies_metadata.csv"
    if os.path.exists(data_file):
        ImportMovieMetata.import_data(data_file)
    else:
        print("Not found data file " + str(data_file))

