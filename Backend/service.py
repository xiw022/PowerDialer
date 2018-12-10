#! /usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """web service"""

import json
import random
import sys



from db import db


reload(sys)
sys.setdefaultencoding('utf-8')

class Service(object):
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
