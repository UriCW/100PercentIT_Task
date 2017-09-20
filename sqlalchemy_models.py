# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String, text
from sqlalchemy import and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime, timedelta


Base = declarative_base()
metadata = Base.metadata

class AcctV9(Base):
    __tablename__ = 'acct_v9'

    tag = Column(Integer, primary_key=True, nullable=False)
    class_id = Column(String(16), primary_key=True, nullable=False)
    mac_src = Column(String(17), primary_key=True, nullable=False)
    mac_dst = Column(String(17), primary_key=True, nullable=False)
    vlan = Column(Integer, primary_key=True, nullable=False)
    as_src = Column(Integer, primary_key=True, nullable=False)
    as_dst = Column(Integer, primary_key=True, nullable=False)
    ip_src = Column(String(15), primary_key=True, nullable=False)
    ip_dst = Column(String(15), primary_key=True, nullable=False)
    port_src = Column(Integer, primary_key=True, nullable=False)
    port_dst = Column(Integer, primary_key=True, nullable=False)
    tcp_flags = Column(Integer, nullable=False)
    ip_proto = Column(String(6), primary_key=True, nullable=False)
    tos = Column(Integer, primary_key=True, nullable=False)
    packets = Column(Integer, nullable=False)
    bytes = Column(BigInteger, nullable=False)
    flows = Column(Integer, nullable=False)
    stamp_inserted = Column(DateTime, primary_key=True, nullable=False)
    stamp_updated = Column(DateTime)
    

class NeutronFipAudit(Base):
    __tablename__ = 'neutron_fip_audit'

    ID = Column(Integer, primary_key=True)
    UUID = Column(String(255))
    PROJECT = Column(String(255))
    IP = Column(String(32), index=True)
    TIMESTAMP = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))


class NeutronSnatAudit(Base):
    __tablename__ = 'neutron_snat_audit'

    ID = Column(Integer, primary_key=True)
    UUID = Column(String(255))
    PROJECT = Column(String(255))
    IP = Column(String(32), index=True)
    TIMESTAMP = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
