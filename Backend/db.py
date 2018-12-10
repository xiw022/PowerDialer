#! /usr/bin/env python
# -*- coding: utf-8 -*-


__doc__ = """db"""

import time
import traceback

import MySQLdb




class DB(object):
    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

        self._connect()


    def _connect(self):
        self.conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset='utf8')
        cursor = self.conn.cursor()

        # Enforce UTF-8 for the connection.
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
        self.conn.commit()


    def _reconnect(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute('SET NAMES utf8mb4')
        except:
            self._connect()


    def query(self, sql):
        cursor = self.conn.cursor()

        rows = None
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
        except:
            self._reconnect()
            logger.error('%s' % traceback.format_exc())
            logger.error('sql: %s', sql)
            return None
        else:
            return rows


    def write(self, sql):
        conn = self.conn
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
            self._reconnect()
            logger.error('%s' % traceback.format_exc())
            logger.error('sql: %s', sql)
            return False
        else:
            return True

    def get_patient_data(self, num_list):
        """随机获取未标注的样本"""
        sql = """SELECT *
            FROM patientnew
            WHERE id not in (select id from callnew)
            ORDER BY id LIMIT %d""" % (num_list)

        rows = db.query(sql)
        if rows is None:
            return None

        patients = []
        for row in rows:
            patient = {}
            
            id = row[0]
            firstname = row[1]
            lastname = row[2]
            dob = row[3]
            phone = row[4]
            primary_payer = row[5]
            medicare= row[6]
            hbac= row[7]
            timezone = row[8]

            patient['id'] = id
            patient['firstname'] = firstname
            patient['lastname'] = lastname
            patient['dob'] = dob
            patient['phone'] = phone
            patient['primary_payer'] = primary_payer
            patient['medicare'] = medicare
            patient['hba1c'] = hbac
            patient['timezone'] = timezone
            patients.append(patient)
        return patients


    def close(self):
        self.conn.close()


db = DB('localhost', 3306, 'root', '940216', 'power_dialer')
