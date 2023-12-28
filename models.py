#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 19:16:07 2023

"""
from sqlalchemy import (
    Integer,
    String,
    Column,
    Boolean,
    DateTime,
    Text,
    ForeignKey
)
from sqlalchemy.orm import relationship
from __init__ import db


class Target(db.Model):
    __tablename__ = "target"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    host = Column(String, unique=True, nullable=False)
    port = Column(Integer, default=443)
    ssl = Column(Boolean, default=True)

    last_scan = Column(DateTime, nullable=True)
    high = Column("High", Integer, default=0)
    medium = Column("Medium", Integer, default=0)
    low = Column("Low", Integer, default=0)
    informational = Column("Informational", Integer, default=0)
    false_positives = Column("False Positives", Integer, default=0)

    scan = relationship("Scan", back_populates="target", order_by='Scan.id.desc()')

    def __str__(self):
        return self.host

    def __repr__(self):
        return self.host


class Scan(db.Model):
    __tablename__ = "scan"
    id = Column(Integer, primary_key=True)
    version = Column(String)
    generated = Column(String)
    alerts = Column(Text)

    high = Column("High", Integer, default=0)
    medium = Column("Medium", Integer, default=0)
    low = Column("Low", Integer, default=0)
    informational = Column("Informational", Integer, default=0)
    false_positives = Column("False Positives", Integer, default=0)

    target_id = Column(Integer, ForeignKey("target.id"))
    target = relationship("Target", back_populates="scan")

    def __str__(self):
        return f"Scan generated: {self.generated}"

    def __repr__(self):
        return self.__str__()
