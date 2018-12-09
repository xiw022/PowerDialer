#! /usr/bin/env python
# -*- coding: utf-8 -*-


__doc__ = """database class"""

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
            
            print "query failed"
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
            print "query failed"
            return False
        else:
            return True

    def get_patient_data(self, num_list):
        
        sql = """SELECT *
            FROM patientnew
            WHERE id not in (select id from callnew where outcome='ENROLLED' or outcome='REJECTED')
            ORDER BY RAND() LIMIT %d""" % (num_list)

        rows = db.query(sql)
        if rows is None:
            return None

        patients = []
        for row in rows:
            patient = {}
            
            ID = row[0]
            firstname = row[1]
            lastname = row[2]
            dob = row[3]
            phone = row[4]
            primary_payer = row[5]
            medicare= row[6]
            hbac= row[7]
            timezone = row[8]

            patient['id'] = ID
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


    def get_patient_byid(self, ID):
   
        sql = """SELECT *
            FROM patientnew
            WHERE id = %s """ % (ID)

        rows = db.query(sql)
        if rows is None:
            return None

        patient = {}

        row=rows[0]

        ID = row[0]
        firstname = row[1]
        lastname = row[2]
        dob = row[3]
        phone = row[4]
        primary_payer = row[5]
        medicare= row[6]
        hbac= row[7]
        timezone = row[8]

        patient['id'] = ID
        patient['firstname'] = firstname
        patient['lastname'] = lastname
        patient['dob'] = dob
        patient['phone'] = phone
        patient['primary_payer'] = primary_payer
        patient['medicare'] = medicare
        patient['hba1c'] = hbac
        patient['timezone'] = timezone

        return patient




    def insert_patientdata(self, line):

        datalist=line.split(',')
        

        ID, firstname, lastname, dob, phone, primary_payer, medicare, hbac, timezone = datalist

        hbac1=float(hbac)

        

    

        sql = """INSERT INTO patientnew (id, firstname, lastname, dob, phone, primary_payer, medicare, hba1c, timezone) VALUES %s"""
        
        
        values = "('%s', '%s', '%s', '%s', '%s', '%s', '%s', %f, '%s')" % (ID.strip(), firstname, lastname, dob, phone, primary_payer, medicare, hbac1, timezone)
        
        sql = sql % values



        return self.write(sql)





    def insert_calldata(self, ID, start_time, end_time, outcome):

        
        patient=self.get_patient_byid(ID)

        if outcome=="ENROLLED":
            enrolledat=end_time
            rejectedat=''
        elif outcome=="REJECTED":
            enrolledat=''
            rejectedat=end_time
        elif outcome=="VOICEMAIL":
            enrolledat=''
            rejectedat=''


        calledat=start_time

        ID = patient['id'] 
        firstname = patient['firstname'] 
        lastname = patient['lastname'] 
        dob = patient['dob'] 
        phone = patient['phone'] 
        primary_payer = patient['primary_payer'] 
        medicare = patient['medicare'] 
        hbac = patient['hba1c'] 
        timezone = patient['timezone']




        sql = """INSERT INTO callnew (id, firstname, lastname, outcome, enrolledat, rejectedat, calledat, dob, phone, primary_payer, medicare, hba1c, timezone) VALUES %s"""


        
        
        values = "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %f, '%s')" % (ID, firstname, lastname, outcome, enrolledat, rejectedat, calledat, dob, phone, primary_payer, medicare, hbac, timezone)
        
        sql = sql % values

        

        return self.write(sql)

        

    def close(self):
        self.conn.close()



    


db = DB('localhost', 3306, 'root', '940216', 'power_dialer')
