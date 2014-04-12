#### The reference code is created by web.py and there are a lot difference here and now it just gives me a overall frame.
#coding: utf-8
from django.db import models
from django.utils import timezone

##db = web.database(dbn='postgresql', db="chat.db")	need to be changed to my db.
class DBManage(object):
	@classmethod
	def table(cls):
		return cls.__name__.lower()

	@classmethod
	def get_by_id(cls, id):
		itertodo = db.select(cls.table(), where="id=$id", vars=locals())
		return next(iter(itertodo), None)

	@classmethod
	def get_all(cls):
		return db.select(cls.table())

	@classmethod
	def create(cls, **kwargs):
		return db.insert(cls.table(), **kwargs)

	@classmethod
	def update(cls, **kwargs):
		db.update(cls.table(), where="id=$id", vars={"id": kwargs.pop('id')}, **kwargs)
	
	@classmethod
	def delete(cls, id):
		db.delete(cls.table(), where="id=$id", vars=locals())


class User(DBManage):
	id = None
	username = None
	password = None
	registed_time = None
	level = None

	@classmethod
	def get_by_username_password(cls, username, password):
		itertodo = db.select(
			cls.table(), 
			where="username=$username and password=$password", 
			vars=locals()
		)
		return next(iter(itertodo))	##why there is a var None in the reference code?
	

class Topic(DBMange):
	id = None
	title = None
	created_time = None
	owner = None
	allowed_user = None	#add privacy control

class Message(DBManage):
	id = None
	content = None
	topic_id = None
	user_id = None
	reply_to = None
	created_time = None
	life = None	#add lifespan to message. automatically delete history messages.

	@classmethod
	def get_by_topic(cls, topic_id):
		now = timezone.now()
		return db.select(
			cls.table(), 
			where="topic_id=$topic_id and now-created_time<life",
			vars=locals()
		)

