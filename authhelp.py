import model

def auth_admin(user):
	emails=['pramodmahapude@gmail.com','jain.mayu333@gmail.com']
	email=user.email()
	if email in emails:
		return True
		
	return False
