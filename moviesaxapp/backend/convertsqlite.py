import sqlalchemy as db
from sqlalchemy import desc, func
from sqlalchemy.dialects.postgresql import insert
import datetime
import logging
try:
    from .config import *
except:
    from config import *
import traceback

class ImportFromSqlLite(object):
    def __int__(self):
        pass

    @staticmethod
    def convert_file(from_file):
        db_engine, connection = get_static_connection()
        table_name = "vidname_cid"
        vid_table = db.Table(table_name, db.MetaData(), autoload=True, autoload_with=db_engine)
        update_time = datetime.datetime.utcnow()
        lines = open(from_file, 'r').readlines()
        try:
            for line in lines:
                line_arr = line.split(",")
                id = line_arr[0]
                file_name = line_arr[1]
                cid = line_arr[-1]
                query = insert(vid_table).values(
                    filename = file_name,
                    cid = cid,
                    update_time = str(update_time)
                )
                connection.execute(query)
        except:
            logging.error("Unable to import  " + str(traceback.print_exc()))


def run_import():
    file1 = "/home/tung/dataset1.csv"
    file2 = "/home/tung/dataset2.csv"
    imp = ImportFromSqlLite()
    imp.convert_file(file1)
    imp.convert_file(file2)



if __name__ == '__main__':
    logging.info("Start running")
    set_log()
    run_import()