import unittest
from sqlalchemy_models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,and_,or_
from sqlalchemy.sql import func
from datetime import datetime,timedelta

class TestModel(unittest.TestCase):
    Session = sessionmaker()

    
    def test_sums_on_object(self):
        session=self.Session()
        some_date = datetime.strptime('2017-08-04 16:35:02' , '%Y-%m-%d %H:%M:%S')
        some_ip = '185.74.72.9'
        tots = AcctV9.sum_bytes_by_ip_and_time_window(session,some_date,some_ip)
        #print "Tots: "+str(tots)


    def get_audit(self,audit,projects):
        """
            appends entries from audit tables (neutron_fip_audit,neutron_snat_audit) to projects dictionary
            and returns an updated dictionary
        """
        for e in audit:
            proj=e.PROJECT
            ip=e.IP
            time=e.TIMESTAMP
            if proj in projects:
                projects[proj].append( (ip,time) )
            else:
                projects[proj]=[ (ip,time) ]
        return projects

    def group_audits(self):
        """
            groups both audit tables into a dictionary of a list of tuples.
            eg. projects[41eba6207073452e87208ee8be8ffa2f] = [(127.0.0.1, 2017-01-01 08:00:00), (127.0.0.1,2017...]

            returns : { 
                project_id:[(ip,timestamp),(ip2,timestamp2)]...,
                project_id2:[(ip3,timestamp3),(ip4,timestamp4)]...,
                ...
            }
        """
        session=self.Session()
        projects={}
        fip_audit=session.query(NeutronFipAudit)
        snat_audit=session.query(NeutronSnatAudit)
        projects=self.get_audit(fip_audit,projects)
        projects=self.get_audit(snat_audit,projects)
        return projects


    
    def construct_conditions(self,values):
        """
            Constructs query filter conditions from a list of tuples [(ip,time),(...]
            returns conditions to be used by query filter
            or_( 
                _and(stamp_updated >= time - 5minute, stamp_updated <= time, or_(ip_src==ip, ip_dst==ip) ),
                _and(stamp_updated >= time2 - 5minute, stamp_updated <= time2, or_(ip_src==ip2, ip_dst==ip2) ),
                ...
                )
        """
        conditions=[]
        for idx,val in enumerate(values):
            cond=[]
            ip=val[0]
            time_window_end=val[1]
            time_window_start=time_window_end-timedelta(minutes=5)
            cond.append(AcctV9.stamp_updated >= time_window_start)
            cond.append(AcctV9.stamp_updated <= time_window_end)
            cond.append(or_(AcctV9.ip_src==ip,AcctV9.ip_dst==ip))
            condition=and_(*cond)
            conditions.append(condition)
        return or_(*conditions)

            #cond=and_(AcctV9.stamp_updated >= time_window_start , AcctV9.stamp_updated <=time_window_end, \
            #or_(AcctV9.ip_src==ip,AcctV9.ip_dst=ip) )


    def disabled_test_queries(self):
        """
            Test total bytes for a single project
        """
        session=self.Session()
        projects_grouped=self.group_audits()
        test_project_id='81e6857ae53a4dbebf1908ccff7793da'
        test_project_values=projects_grouped[test_project_id]
        conditions=self.construct_conditions(test_project_values)
        tots=session.query(func.sum(AcctV9.bytes)).filter(conditions)
        print test_project_id+" bytes: "+str(tots.scalar() )

    def test_all_projects_totals(self):
        session=self.Session()
        projects_grouped=self.group_audits()
        for project_id in projects_grouped:
            project_audit_data=projects_grouped[project_id]
            conditions=self.construct_conditions(project_audit_data)
            total_bytes=session.query(func.sum(AcctV9.bytes)).filter(conditions).scalar()
            print "Project {0} total bytes {1}".format(project_id,str(total_bytes) )
    
    def setUp(self):
        engine = create_engine('mysql://uri:password123@localhost/pmacct', echo=False)
        self.Session.configure(bind=engine)

if __name__=="__main__":
    unittest.main()

