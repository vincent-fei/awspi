#-*- coding:UTF-8 -*-
from django.shortcuts import render, render_to_response
import MySQLdb
import sys

# Create your views here.
class DBConnector(object):
    def __init__(self, host, port, user, passwd, db, charset='utf8'):
        self.conn = MySQLdb.connect(
                host = host,
                port = port,
                user = user,
                passwd = passwd,
                db = db,
                charset = charset)

    def get_cursor(self):
        return self.conn.cursor()

    def query(self, sql):
        cursor = self.get_cursor()
        try:
            cursor.execute(sql, None)
            result = cursor.fetchall()
        except Exception, e:
            logging.error("mysql query error: %s", e)
            return None
        finally:
            cursor.close()
        return result

    def execute(self, sql, param=None):
        cursor = self.get_cursor()
        try:
            cursor.execute(sql, param)
            self.conn.commit()
            affected_row = cursor.rowcount
        except Exception, e:
            logging.error("mysql execute error: %s", e)
            return 0
        finally:
            cursor.close()
        return affected_row

    def executemany(self, sql, params=None):
        cursor = self.get_cursor()
        try:
            cursor.executemany(sql, params)
            self.conn.commit()
            affected_rows = cursor.rowcount
        except Exception, e:
            logging.error("mysql executemany error: %s", e)
            return 0
        finally:
            cursor.close()
        return affected_rows

    def close(self):
        try:
            self.conn.close()
        except:
            pass

    def __del__(self):
        self.close()


def ListInstances(request):
    # get all instances
    mysql = DBConnector(host='127.0.0.1', port=3306, user='awspi', passwd='changyou.com', db='awspi', charset='utf8')
    sql = "select * from ec2pi_instances;"
    instances = mysql.query(sql)

    return render_to_response('listinstance.html',{'instances':instances})

def ListVolumes(request):
    # get all volumes
    mysql = DBConnector(host='127.0.0.1', port=3306, user='awspi', passwd='changyou.com', db='awspi', charset='utf8')
    sql = "select * from ec2pi_volumes;"
    volumes = mysql.query(sql)

    return render_to_response('listvolume.html',{'volumes':volumes})

def ListIP(request):
    mysql = DBConnector(host='127.0.0.1', port=3306, user='awspi', passwd='changyou.com', db='awspi', charset='utf8')
    sql = "select * from ec2pi_addresses;"
    addresses = mysql.query(sql)

    return render_to_response('listip.html',{'addresses':addresses})
