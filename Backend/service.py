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

    



if __name__ == '__main__':
    service = Service()
    