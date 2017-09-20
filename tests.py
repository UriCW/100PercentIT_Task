import unittest
from sqlalchemy_models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,and_,or_
from sqlalchemy.sql import func
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

    def sum_bytes_by_ip_and_time_window(self,session,date,ip):
        total_bytes=session.query(func.sum(AcctV9.bytes )).filter(
            AcctV9.stamp_updated >= date -timedelta(minutes=5),
            AcctV9.stamp_updated <= date, 
            or_(AcctV9.ip_src == ip, AcctV9.ip_dst ==ip)
        )
        return total_bytes.scalar()

    #Tests my query skillz 
    def test_queries(self):
        session=self.Session()
        some_date = datetime.strptime('2017-08-04 16:35:02' , '%Y-%m-%d %H:%M:%S')
        some_ip = '185.74.72.9'
        entries=self.entries_by_ip_and_time_window(session,some_date,some_ip)
        for entry in entries:
            print entry.ip_src+" -> "+entry.ip_dst+" "+str(entry.bytes) +" "+str(entry.stamp_updated)
        
    def test_sums(self):
        session=self.Session()
        some_date = datetime.strptime('2017-08-04 16:35:02' , '%Y-%m-%d %H:%M:%S')
        some_ip = '185.74.72.9'
        total_bytes=self.sum_bytes_by_ip_and_time_window(session,some_date,some_ip)
        print "total bytes: "+str(total_bytes)
    
    def test_sums_on_object(self):
        session=self.Session()
        some_date = datetime.strptime('2017-08-04 16:35:02' , '%Y-%m-%d %H:%M:%S')
        some_ip = '185.74.72.9'
        tots = AcctV9.sum_bytes_by_ip_and_time_window(session,some_date,some_ip)
        print "Tots: "+str(tots)

    def test_show_totals(self):
        session=self.Session()
        ret=[]
        fip_audit=session.query(NeutronFipAudit)
        snat_audit=session.query(NeutronSnatAudit)
        for entry in fip_audit:
            ip=entry.IP
            project=entry.PROJECT
            timestamp=entry.TIMESTAMP
            total_bytes=AcctV9.sum_bytes_by_ip_and_time_window(session,timestamp,ip)
            ret.append({'ip':ip,'project':project,'timestamp':timestamp,'totalbytes':total_bytes  })

        for r in ret:
            print r

    def setUp(self):
        engine = create_engine('mysql://uri:password123@localhost/pmacct', echo=True)
        self.Session.configure(bind=engine)

if __name__=="__main__":
    unittest.main()

