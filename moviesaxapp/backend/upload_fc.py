from pygate_grpc.client import PowerGateClient
from pygate_grpc.ffs import get_file_bytes, bytes_to_chunks

from sqlalchemy.dialects.postgresql import insert
import traceback
from pathlib import Path
import time
try:
    from .config import *
except:
    from config import *
import datetime

c = PowerGateClient(POWD_HOST)

class PushFileToFc(object):
    def __int__(self):
        pass

    def push_file(self, abs_file_name):
        try:
            iter = get_file_bytes(abs_file_name)
            logging.info("Adding file to IPFS (hot storage)...")

            res = c.ffs.stage(bytes_to_chunks(iter), TOKEN)
            logging.info(res)
            logging.info("Pushing file: " + str(abs_file_name) + "  to FFS...")

            c.ffs.push(res.cid, TOKEN)

            file_name = abs_file_name.split("/")[-1]
            db_engine, connection = get_static_connection()
            table_name = "vidname_cid"
            vid_table = db.Table(table_name, db.MetaData(), autoload=True, autoload_with=db_engine)
            update_time = datetime.datetime.utcnow()
            try:
                query = insert(vid_table).values(
                    filename=file_name,
                    cid=res.cid,
                    update_time=str(update_time)
                )
                connection.execute(query)
            except:
                logging.error("Unable to insert  " + str(traceback.print_exc()))
            time.sleep(SLEEP_BETWEN_PUSH_FILE)
            logging.info("Push " + file_name + " done")
        except:
            logging.info("bad happen" + str(traceback.print_exc()))

    def push_files_from_folder(self, from_folder,filter):
        pathlist = Path(from_folder).glob('**/*.*')
        if filter:
            pathlist = Path(folder).glob(filter)
        logging.info("from " + str(pathlist))
        for path in pathlist:
            path_in_str = str(path)
            logging.info(path_in_str)
            self.push_file(path_in_str)

    def save_file(self,cid,filename):
        logging.info("Retrieving file " + cid + " from FFS.")
        file_ = c.ffs.get(cid,TOKEN)
        f = open(filename, "wb")
        for f_ in file_:
            f.write(f_)
        f.close()


if __name__ == "__main__":

    pf = PushFileToFc()
    #folder = "/home/tung/Downloads/publicmovies212/"
    #folder = "/mnt/sdc/openmovies/publicmovies212/"
    #folder = "/mnt/sdc/publicmovies212"
    folder = "/home/tung/test/"
    pf.push_files_from_folder(folder,filter=None)

