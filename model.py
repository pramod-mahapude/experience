from google.appengine.ext import ndb

class Company(ndb.Model):
	companyname=ndb.StringProperty()
	noofrounds=ndb.StringProperty()
	noofselectedcandidates=ndb.StringProperty()
	stipend=ndb.StringProperty()
	criteria=ndb.StringProperty()
	tenth=ndb.StringProperty()
	twelth=ndb.StringProperty()
	grad=ndb.StringProperty()
	pgrad=ndb.StringProperty()
	
class Member(ndb.Model):
	name=ndb.StringProperty()
	email=ndb.StringProperty()
	phoneno=ndb.StringProperty()
	type=ndb.StringProperty()
	company=ndb.KeyProperty(Company)
	division=ndb.StringProperty()

class Uploadfiles(ndb.Model):
	filename=ndb.StringProperty()
	company=ndb.KeyProperty(Company)
	name=ndb.StringProperty() #UPDATE HERE
	file_key=ndb.BlobKeyProperty()

'''class Comment(ndb.Model):
	comment=ndb.StringProperty()
	company=ndb.KeyProperty(Company)
	name=ndb.StringProperty()#UPDATE HERE
	date=ndb.DateTimeProperty(auto_now_add=True)'''
	
class Comment(ndb.Model):
	comment=ndb.StringProperty()
	company=ndb.KeyProperty(Company)
	name=ndb.StringProperty()#UPDATE HERE
	date=ndb.DateTimeProperty(auto_now_add=True)
	file_info=ndb.KeyProperty(Uploadfiles)
	mem_key=ndb.KeyProperty(Member)
	
class Companyentry(ndb.Model):
	companyname=ndb.StringProperty()
	noofrounds=ndb.StringProperty()
	stipend=ndb.StringProperty()
	criteria=ndb.StringProperty()

class StudentInfo(ndb.Model):
	stud_key=ndb.StringProperty()
	name=ndb.StringProperty()
	email=ndb.StringProperty()
	phoneno=ndb.StringProperty()
	division=ndb.StringProperty()
	tenth=ndb.StringProperty()
	twelth=ndb.StringProperty()
	grad=ndb.StringProperty()
	pgrad=ndb.StringProperty()
	filename=ndb.StringProperty()
	file_key=ndb.BlobKeyProperty()
	proj1=ndb.StringProperty()
	proj2=ndb.StringProperty()
	proj3=ndb.StringProperty()