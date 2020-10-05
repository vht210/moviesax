import sqlalchemy as db
from sqlalchemy import desc, func
try:
    from .config import *
except:
    from config import *

import datetime
import ipfshttpclient

class MovieQuery(object):

    @staticmethod
    def get_movies_cid():
        rs = []
        table_name = 'vidname_cid'
        metadata = db.MetaData()
        db_engine, connection = get_static_connection()
        key_stat_table = db.Table(table_name, metadata, autoload=True, autoload_with=db_engine)
        query_time = datetime.datetime.utcnow()
        query = db.select([
            key_stat_table.columns.filename,
            key_stat_table.columns.cid,
            key_stat_table.columns.update_time,

        ]).order_by(key_stat_table.columns.filename)
        rs_proxy = connection.execute(query)
        rows = rs_proxy.fetchall()
        count = 0
        dict_filename_cid={}
        dict_filename_updatetime={}
        if rows:
            for row in rows:
                movie_file_name = str(row[0])
                cid = str(row[1]).replace("\n","")
                if movie_file_name not in dict_filename_cid:
                    dict_filename_cid[movie_file_name] = [cid]
                    dict_filename_updatetime[movie_file_name] = str(row[2])
                #else:
                #    tmp_cid_lst = dict_filename_cid[movie_file_name]
                #    tmp_cid_lst.append(cid)
                #    dict_filename_cid[movie_file_name] = tmp_cid_lst

        for k in sorted(dict_filename_cid.keys()):
            count = count + 1
            temp_dict = {"count": count,
                         "file_name": k,
                         "movie_name": MovieQuery.get_movie_from_filename(k),
                         "cid":dict_filename_cid[k],
                         "update_time": dict_filename_updatetime[k]
                         }
            rs.append(temp_dict)
        connection.close()
        db_engine.dispose()
        return rs

    @staticmethod
    def get_movie_from_filename(filename):
        return str(filename).split(".")[0].replace("_"," ")


    @staticmethod
    def create_video_in_cache(cid,video_name):
        client = ipfshttpclient.connect()
        destination = "../../static/video/" + video_name
        #client.get(cid,)