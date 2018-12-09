#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Tencent Inc.
# Author: Zhenlong Sun (richardsun@tencent.com)

__doc__ = """web service"""

import json
import random
import sys



from db import db


reload(sys)
sys.setdefaultencoding('utf-8')

class Service(object):
    """为界面提供接口，返回结果为json格式"""
    def __init__(self):
        self.data=[]
        # self.task_confs = []
        # self._cache()


    def get_patient_data(self, num_list):
        """
        return patient list from the database
        """
        

       
   
        
        patients = db.get_patient_data(num_list)
        
        if patients is None:
            return None, 'db failed.'

        return patients, ''




    def load_newpatient_data(self, line):
            
            if not db.insert_patientdata(line):
                
                return False, 'insert_patientdata failed.'
            return True, ''



    def load_calledpatient_data(self, ID, start_time, end_time, outcome):
            
            if not db.insert_calldata(ID, start_time, end_time, outcome):
                
                return False, 'insert_calldata failed.'
            return True, ''

    # def _cache(self):
    #     """载入所有taxonomy，cache起来，加速后续请求"""
    #     for task_conf in g_task_conf_manager.task_confs.task_confs:
    #         task_conf_dict = {}
    #         task_conf_dict['name'] = task_conf.name
    #         task_conf_dict['owners'] = []
    #         for owner in task_conf.owners:
    #             task_conf_dict['owners'].append(owner)
    #         task_conf_dict['labelers'] = []
    #         for labeler in task_conf.labelers:
    #             task_conf_dict['labelers'].append(labeler)
    #         task_conf_dict['active_learning_on'] = task_conf.active_learning_on

    #         if task_conf.type == task_conf_pb2.CATEGORY:
    #             task_conf_dict['type'] = conf.task_type_category
    #             task_conf_dict['taxonomy'] = open("conf/" + task_conf.taxonomy_file_name, 'r').read()
    #         else:
    #             task_conf_dict['type'] = conf.task_type_keyword
    #             task_conf_dict['keyword_score_lowerbound'] = task_conf.keyword_score_lowerbound
    #             task_conf_dict['keyword_score_upperbound'] = task_conf.keyword_score_upperbound

    #         self.task_confs.append(task_conf_dict)

'''
    def get_task_confs(self):
        return self.task_confs

    @staticmethod
    def is_in_task(task_name, rtx):
        """ rtx是否该任务的owner或者labeler"""
        task_conf = g_task_conf_manager.task_conf_dict[task_name]
        for owner in task_conf.owners:
            if owner == rtx:
                return True
        for labeler in task_conf.labelers:
            if labeler == rtx:
                return True
        return False

    
    def get_unlabeled_data(self, task_name, rtx, num_samples):
        """样本分配机制
            - owner :  任何人没标注过的数据
            - labeler : 任何人没标过的数据 + 专家标过的数据
        """
        # 参数校验
        if num_samples <= 0:
            logger.error("num_samples is invalid. num_samples=%d" % num_samples)
            return None, "num_samples is invalid. num_samples=%d" % num_samples

        if not Service.is_in_task(task_name, rtx):
            logger.error('rtx not in task. task_name=%s, rtx=%s' % (task_name, rtx))
            return None, "rtx not in task."

        owner_sample_ratio = g_task_conf_manager.get_owner_sample_ratio(task_name)

        samples = []
        is_owner = g_task_conf_manager.is_owner(task_name, rtx)
        if is_owner:
            samples = db.get_unlabeled_sample(task_name, num_samples)
            if samples is None:
                logger.error('get_unlabeled_sample failed.')
                return None, 'db failed.'
        else:
            num_owner_samples = 0
            for i in range(num_samples):
                if random.random() < owner_sample_ratio:
                    num_owner_samples += 1
            logger.debug("num_owner_samples: %d" % num_owner_samples)
            owner_samples = []
            if num_owner_samples > 0:
                owner_samples = db.get_owner_sample(task_name, num_owner_samples, rtx)
                if owner_samples is None:
                    logger.error('get_owner_sample failed.')
                    return None, 'db failed.'
                samples.extend(owner_samples)
            num_new_samples = num_samples - len(owner_samples)
            logger.debug("num_owner_samples: %d, num_new_samples: %d" % (len(owner_samples), num_new_samples))
            unlabeled_samples = db.get_unlabeled_sample(task_name, num_new_samples)
            if unlabeled_samples is None:
                logger.error('get_unlabeled_sample failed.')
                return None, 'db failed.'
            samples.extend(unlabeled_samples)
        return samples, ''


    def update_aritificial_tag(self, task_name, id, artificial_tags, rtx):
        """" 更新标注结果到DB中，存在则覆盖
             artificial_tags example: [{"artificial_tag" : "女装", "score" : 3},{"artificial_tag" : "时尚", "score" : 1}]"""
        if not Service.is_in_task(task_name, rtx):
            logger.error('rtx not in task. task_name=%s, rtx=%s' % (task_name, rtx))
            return False, 'rtx not in task'

        is_owner = g_task_conf_manager.is_owner(task_name, rtx)
        is_standard = 0
        if is_owner:
            is_standard = 1

        # 判断是否存在，存在则删掉
        if not db.delete_artificial_tag(task_name, id, rtx):
            err = "failed to delete. task_name=%s" % task_name
            logger.error(err)
            return False, err

        artificial_tag_list = []
        for artificial_tag in artificial_tags:
            artificial_tag_list.append((id, artificial_tag["artificial_tag"],
                                        artificial_tag["score"], rtx, is_standard))

        if not db.insert_artificial_tag(task_name, artificial_tag_list):
            logger.error("insert_artificial_tag failed.")
            return False, 'insert_artificial_tag failed.'
        return True, ''
'''


if __name__ == '__main__':
    service = Service()
    #print json.dumps(service.get_task_confs(), ensure_ascii=False).encode('utf8')
    #u = service.get_unlabeled_data('20170903keyword', 'richardsun', 4)
    #js = json.dumps(u, ensure_ascii=False).encode('utf8')
    #print js

    """
    artificial_tags = [{"artificialTag" : "网络游戏", "score" : 2}, {"artificialTag" : "游戏", "score" : 1}]
    print service.update_aritificial_tag('20170903keyword', 0, artificial_tags, 'richardsun')
    """