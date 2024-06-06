from sqlalchemy import (
	Column,
	Integer,
	String,
	DateTime,
	Table,
	ForeignKey,
	func
)

from src.config   import settings
from src.database import metadata

t_fingerprint = Table(
	settings.FP_TABLE,
	metadata,
	Column('id',         Integer, primary_key=True, index=True),
	Column('visitor_id', Integer),
	Column('user_id',    Integer),
	Column('user_agent', String),
	Column('ip',         String, nullable=True),
	Column('hash',       String),
	Column('created',    DateTime(timezone=True), default=func.now()),
)

t_action = Table(
	settings.ACTION_TABLE,
	metadata,
	Column('id',           Integer, primary_key=True, index=True),
	Column('name',         String),
	Column('description',  String),
	Column('created',      DateTime(timezone=True), default=func.now(), nullable=False),
)

t_log = Table(
	settings.LOG_TABLE,
	metadata,
	Column('id',             Integer, primary_key=True, index=True),
	Column('action_id',      ForeignKey(f'{settings.ACTION_TABLE}.id', ondelete='CASCADE'), nullable=False),
	Column('fingerprint_id', ForeignKey(f'{settings.FP_TABLE}.id',     ondelete='CASCADE'), nullable=False),
	Column('created',        DateTime(timezone=True), default=func.now(), nullable=False),
)
