#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Tencent Inc.
# Author: Zhenlong Sun (richardsun@tencent.com)

__doc__ = """数据库类"""

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
        """随机获取未标注的样本"""
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
        """随机获取未标注的样本"""
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

'''
    def create_table(self, task_name):
        """创建表"""
        # Sample: 样本表
        sql = """CREATE TABLE IF NOT EXISTS `%s` (
                `id` bigint NOT NULL COMMENT '样本id',
                `text` longtext NOT NULL COMMENT '样本文本，即document',
                `comment` varchar(255) NOT NULL COMMENT '用户自定义内容',
                `createdTime` datetime NOT NULL COMMENT '创建时间',
                primary key(id) 
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8 
                """ % (conf.sample_table_name % task_name)
        if not self.write(sql):
            logger.error("create table Sample failed. sql: %s" % sql)
            return False

        # CandidateTag: 候选标签表，抽取的关键词或者active learning分类器的预测类目，一个样本对应多个predictedTag
        sql = """CREATE TABLE IF NOT EXISTS `%s` (
                `id` bigint NOT NULL COMMENT '样本id',
                `predictedTag` varchar(255) NOT NULL COMMENT '候选关键词或者弱分类器预测的类目',
                `predictedWeight` float NOT NULL COMMENT '权重',
                `createdTime` datetime NOT NULL COMMENT '创建时间',
                primary key(id, predictedTag),
                foreign key (id) references %s(id) 
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8 
                """ % (conf.candidate_tag_table_name % task_name, conf.sample_table_name % task_name)
        if not self.write(sql):
            logger.error("create table CandidateTag failed. sql: %s" % sql)
            return False

        # AritificialTag: 人工标注结果表，一个样本对应多个artificialTag
        sql = """CREATE TABLE  IF NOT EXISTS `%s` (
                `id` bigint NOT NULL COMMENT '样本id',
                `artificialTag` varchar(255) NOT NULL COMMENT '人工标注结果，关键词或者类目',
                `score` int NOT NULL COMMENT '分数',
                `rtx` varchar(255) NOT NULL COMMENT 'rtx',
                `isStandard` int NOT NULL COMMENT '是否为owner标注，1表示是',
                `createdTime` datetime NOT NULL COMMENT '创建时间',
                primary key(id, artificialTag, rtx),
                foreign key (id) references %s(id) 
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8
                """ % (conf.artificial_tag_table_name % task_name, conf.sample_table_name % task_name)
        if not self.write(sql):
            logger.error("create table AritificialTag failed. sql: %s" % sql)
            return False

        sql = """CREATE OR REPLACE VIEW %s AS SELECT s.id AS id, text 
                FROM %s s LEFT JOIN %s a ON s.id = a.id 
                WHERE a.id is NULL""" % (conf.unlabeled_sample_view_name % task_name,
                                         conf.sample_table_name % task_name,
                                         conf.artificial_tag_table_name % task_name)
        if not self.write(sql):
            logger.error("create view failed. sql: %s" % sql)
            return False

        return True


    def get_max_id(self, task_name):
        """ 返回值:
                None - 出错
                -1   - 不存在记录
                >=0  - 最大id
        """
        sql = """select max(id) as maxId from %s""" % (conf.sample_table_name % task_name)
        rows = self.query(sql)
        if rows is None or len(rows) != 1:
            return None
        max_id = rows[0][0]

        return max_id if max_id else -1


    def insert_sample(self, task_name, id, text, comment):
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """INSERT INTO %s (id, text, comment, createdTime) VALUES(%d, '%s', '%s', '%s')""" % (
            (conf.sample_table_name % task_name), id, text, comment, cur_time)
        return self.write(sql)


    def insert_candidate_tag(self, task_name, candidate_tag_list):
        if len(candidate_tag_list) == 0:
            return True

        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """INSERT INTO %s (id, predictedTag, predictedWeight, createdTime)
            VALUES %s"""

        values = ""
        for  id, predicted_tag, predicted_weight  in candidate_tag_list:
            values += "(%d,'%s',%f,'%s')," % (id, predicted_tag, predicted_weight, cur_time)

        values = values[:-1]
        sql = sql % (conf.candidate_tag_table_name % task_name, values)
        return self.write(sql)

    def delete_artificial_tag(self, task_name, id, rtx):
        sql = """delete from %s where id = %d and rtx = '%s'"""  \
              % (conf.artificial_tag_table_name % task_name, id, rtx)
        return self.write(sql)

    def insert_artificial_tag(self, task_name, artificial_tag_list):
        if len(artificial_tag_list) == 0:
            return True
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """INSERT INTO %s (id, artificialTag, score, rtx, isStandard, createdTime)
            VALUES %s"""
        values = ""
        for id, artificial_tag, score, rtx, is_standard in artificial_tag_list:
            values += "(%d, '%s', %d, '%s', %d, '%s')," % (id, artificial_tag, score, rtx, is_standard, cur_time)
        values = values[:-1]
        sql = sql % (conf.artificial_tag_table_name % task_name, values)
        return self.write(sql)


    def get_sample(self, task_name):
        sql = """select id, text, comment from %s """ % (conf.sample_table_name % task_name)
        return self.query(sql)


    def get_candidate_tag_by_id(self, task_name, id):
        """结果降序"""
        sql = """select predictedTag, predictedWeight from %s
        where id = %d order by predictedWeight desc""" % ((conf.candidate_tag_table_name % task_name), id)
        rows = self.query(sql)
        if rows is None:
            return None
        candidate_tags = []
        for row in rows:
            candidate_tag = {}
            candidate_tag['predicted_tag'] = row[0]
            candidate_tag['predicted_weight'] = row[1]
            candidate_tags.append(candidate_tag)

        return candidate_tags


    def get_labeled_data(self, task_name):
        sql = """select s.id, text, comment, artificialTag, score, isStandard 
        from %s s inner join %s a on s.id = a.id""" % \
        (conf.sample_table_name % task_name, conf.artificial_tag_table_name % task_name)
        return self.query(sql)

    def _join_candidate_tags(self, task_name, rows):
        if rows is None:
            return None

        unlabeled_samples = []
        for row in rows:
            unlabeled_sample = {}
            id = row[0]
            text = row[1]
            candidate_tags = self.get_candidate_tag_by_id(task_name, id)
            if candidate_tags is None:
                return None
            unlabeled_sample['id'] = id
            unlabeled_sample['text'] = text
            unlabeled_sample['candidate_tags'] = candidate_tags
            unlabeled_samples.append(unlabeled_sample)
        return unlabeled_samples

    def get_unlabeled_sample(self, task_name, num_samples):
        """随机获取未标注的样本"""
        sql = """SELECT t1.id as id, text
            FROM %s AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM %s)-(SELECT MIN(id) FROM %s))+(SELECT MIN(id) FROM %s)) AS id) AS t2
            WHERE t1.id >= t2.id
            ORDER BY t1.id LIMIT %d""" % \
              (conf.unlabeled_sample_view_name % task_name,
               conf.unlabeled_sample_view_name % task_name,
               conf.unlabeled_sample_view_name % task_name,
               conf.unlabeled_sample_view_name % task_name,
               num_samples)

        rows = db.query(sql)
        if rows is None:
            return None
        return self._join_candidate_tags(task_name, rows)

    def get_owner_sample(self, task_name, num_samples, rtx):
        """get samples which is labeled by owner and not labeled by rtx"""
        sql = """select id, text from %s where id in 
        (select id from %s where isStandard = 1 and id not in (
        select id from %s where rtx = '%s')) limit %d""" % (
            (conf.sample_table_name % task_name), (conf.artificial_tag_table_name % task_name),
            (conf.artificial_tag_table_name % task_name), rtx, num_samples)

        rows = self.query(sql)
        if rows is None:
            return None
        return self._join_candidate_tags(task_name, rows)


    def get_table_num(self, table_name):
        """获取table大小"""
        sql = """select count(*) from %s""" % (table_name)
        rows = self.query(sql)
        if rows is None:
            logger.error("failed to query. sql=%s" % sql)
            return None
        if len(rows) != 1:
            logger.error("len(rows) expected 1, got %d" % len(rows))
            return None
        return rows[0][0]


    def get_total_sample_num(self, task_name):
        """获取样本总量"""
        return self.get_table_num(conf.sample_table_name % task_name)


    def get_unlabeled_sample_num(self, task_name):
        """获取未标注样本数量"""
        return self.get_table_num(conf.unlabeled_sample_view_name % task_name)


    def get_rtx_labeled_sample_num(self, task_name, date):
        sql = """select rtx, count(distinct id) from %s where createdTime like '%s%%' group by rtx""" % \
              (conf.artificial_tag_table_name % task_name, date)
        rows = self.query(sql)
        if rows is None:
            logger.error("failed to run sql. sql=" % sql)
            return None
        result = []
        for row in rows:
            item = dict()
            item['rtx'] = row[0]
            item['labeled_sample_num'] = row[1]
            result.append(item)
        return result


    def get_presicion_category(self, task_name, rtx, date):
        """计算labeler标注准确率， category类型任务"""
        sql = """select l.artificialTag as labeler_tag, o.artificialTag as owner_tag from 
        %s l, %s o where l.id=o.id and l.isStandard=0 and l.rtx='%s' and 
        l.createdTime like '%s%%' and o.isStandard=1""" % \
        (conf.artificial_tag_table_name % task_name,
         conf.artificial_tag_table_name % task_name,
         rtx, date)

        rows = self.query(sql)
        if rows is None:
            return None

        total_num = 0
        equal_num = 0
        for row in rows:
            total_num += 1
            if row[0] == row[1]:
                equal_num += 1
        precision = -1.0
        if total_num > 0:
            precision = equal_num * 1.0 / total_num
        result = dict()
        result['validate_num'] = total_num
        result['precision'] = precision
        return result

    def get_validate_num_keyword(self, task_name, rtx, date):
        """获取labeler标注样本中校验样本的个数"""
        sql = """select count(distinct l.id) from 
        %s l, %s o where l.id=o.id and l.artificialTag=o.artificialTag and l.isStandard=0 and l.rtx='%s' and 
        l.createdTime like '%s%%' and o.isStandard=1""" % (conf.artificial_tag_table_name % task_name,
         conf.artificial_tag_table_name % task_name,
         rtx, date)

        rows = self.query(sql)
        if rows is None:
            return None

        if len(rows) != 1:
            logger.error("len(rows) expected 1, got %d" % len(rows))
            return None
        return rows[0][0]


    def get_labeler_owner_score_pair_keyword(self, task_name, rtx, date):
        """获取labeler和owner对相同样本相同标签的分数"""
        sql = """select l.score as labeler_score, o.score as owner_score from 
            %s l, %s o where l.id=o.id and l.artificialTag=o.artificialTag and l.isStandard=0 and l.rtx='%s' and 
            l.createdTime like '%s%%' and o.isStandard=1""" % (conf.artificial_tag_table_name % task_name,
        conf.artificial_tag_table_name % task_name, rtx, date)

        rows = self.query(sql)
        if rows is None:
            return None

        return rows


    def delete_great_than_id(self, task_name, id):
        """ 删除大于id的记录，包括Sample, CandidateTag"""
        sql_pattern = """delete from %s where id > %d"""
        if not self.write(sql_pattern % (conf.candidate_tag_table_name % task_name, id)):
            return False
        return self.write(sql_pattern % (conf.sample_table_name % task_name, id))
'''

    


db = DB('localhost', 3306, 'root', '940216', 'power_dialer')
