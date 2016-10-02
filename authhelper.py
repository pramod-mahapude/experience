import model

def is_admin(user):
	emails=['pramodmahapude@gmail.com','jain.mayu333@gmail.com']
	if user.email() in emails:	
		return True
	return False

def is_user(user):
	qry = model.Member.query(model.Member.email == user.email()).get()
	if qry is None:
		return False
	return True
