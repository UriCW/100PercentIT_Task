import unittest
from sqlalchemy_models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,and_,or_
from datetime import datetime,timedelta

class TestModel(unittest.TestCase):
    Session = sessionmaker()

    """
    #Checks that the time delta condition works
    def test_time_delta(self):
        session=self.Session()
        entries=session.query(AcctV9)
        some_date = datetime.strptime('2017-08-04 16:35:02' , '%Y-%m-%d %H:%M:%S')
        for entry in entries:
            if entry.is_in_window(some_date):
                print entry.ip_src+" -> "+entry.ip_dst+" "+str(entry.stamp_updated)
    """

    def entries_by_ip_and_time_window(self,session,date,ip):
        entries=session.query(AcctV9).filter(
            AcctV9.stamp_updated >= date -timedelta(minutes=5),
            AcctV9.stamp_updated <= date, 
            or_(AcctV9.ip_src == ip, AcctV9.ip_dst ==ip)
        )
        return entries


    #Tests my query skillz 
    def test_queries(self):
        session=self.Session()
        some_date = datetime.strptime('2017-08-04 16:35:02' , '%Y-%m-%d %H:%M:%S')
        some_ip = '185.74.72.9'
        entries=self.entries_by_ip_and_time_window(session,some_date,some_ip)
        #entries=session.query(AcctV9).filter(
        #    AcctV9.stamp_updated >= some_date -timedelta(minutes=5),
        #    AcctV9.stamp_updated <= some_date, 
        #    or_(AcctV9.ip_src == some_ip, AcctV9.ip_dst ==some_ip)
        #)
        for entry in entries:
            print entry.ip_src+" -> "+entry.ip_dst+" "+str(entry.bytes) +" "+str(entry.stamp_updated)
        
    
    def setUp(self):
        engine = create_engine('mysql://uri:password123@localhost/pmacct', echo=True)
        self.Session.configure(bind=engine)

if __name__=="__main__":
    unittest.main()

