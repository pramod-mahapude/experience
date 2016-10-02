import webapp2
import basehandler
from google.appengine.api import users
import model
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import urllib
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import mail
import mimetypes
from google.appengine.api import images
from google.appengine.ext import ndb
from urllib import urlretrieve
import os
import authhelper

class RegisterHandler(basehandler.BaseHandler):
    def get(self):
        self.render_template('register.html',users=users)
        
    def post(self):
		name=self.request.POST.get('name')
		email=self.request.POST.get('email')
		emails=['pramodmahapude@gmail.com','jain.mayu333@gmail.com']
		if email in emails:
			type='a'
		else:
			type='u'
		phoneno=self.request.POST.get('phoneno')
		division=self.request.POST.get('division')
		member=model.Member.query(model.Member.email==email).get()
		if member:
			self.abort(403)
		else:
			user=model.Member(name=name,email=email,phoneno=phoneno,type=type,division=division)
			user.put()
			self.redirect('/')
		
class LoginHandler(basehandler.BaseHandler):	
	def get(self):
		user=users.get_current_user()
		if user is None:
			self.render_template('index.html')
		elif authhelper.is_user(user):
			if authhelper.is_admin(user):
				self.redirect('/adminindex')
			else:
				self.redirect('/index')
		else:
			self.redirect('/unauthorized')
		##self.render_template('trial.html',users=users)
		
class GeneralHandler(basehandler.BaseHandler):	
	def get(self):
		self.render_template('index.html',users=users)

class AdminIndexHandler(basehandler.BaseHandler):	
	def get(self):
		self.render_template('adminindex.html',users=users)
		
class MemdisplayHandler(basehandler.BaseHandler):
	@login_required
	def get(self):
		members=model.Member.query().fetch()
		if members:
			self.render_template('memdisplay.html',members=members,users=users)
		else:
			self.abort(403)

class FiledisplayHandler(basehandler.BaseHandler):
	@login_required
	def get(self):
		fileinfo=model.Uploadfiles.query().fetch()
		if fileinfo:
			self.render_template('filedisplay.html',fileinfo=fileinfo,users=users)
		else:
			self.abort(403)
		
	
class FileUpHandler(basehandler.BaseHandler):
	@login_required
	def get(self):
		cnames=model.Company.query()
		upload_url=blobstore.create_upload_url('/upload')
		self.render_template('uploadfile.html',cnames=cnames,
                             users=users,
                             url=upload_url)

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):	
	def post(self):
		user=users.get_current_user()
		email=user.email()
		member=model.Member.query(model.Member.email==email).get()
		upload_files=self.get_uploads('filename')
		blob_info=upload_files[0]
		#filename=self.request.POST.get('filename')
		filename=self.request.POST["filename"].filename
		companyname=self.request.POST.get('cname')
		'''if "None" in companyname:
			uploadfiles=model.Uploadfiles(filename=filename,company=None,name=member.name,file_key=blob_info.key())
			uploadfiles.put();
			self.redirect('/')'''
		#else:
		company=model.Company.get_by_id(int(companyname))
		uploadfiles=model.Uploadfiles(filename=filename,company=company.key,name=member.name,file_key=blob_info.key())
		uploadfiles.put();
		self.redirect('/')
		
class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def post(self):
        key=self.request.POST.get('file_key')
        key=str(urllib.unquote(key))
        blob_info=blobstore.BlobInfo.get(key)
        self.send_blob(blob_info)
	
class CommentHandler(basehandler.BaseHandler):
	def get(self):
		user=users.get_current_user()
		email=user.email()
		member=model.Member.query(model.Member.email == email).get() #information about current user
		file_key=self.request.get('filekey') #file on which comments should be written  
		uploadfile=model.Uploadfiles.get_by_id(int(file_key))
		cname=self.request.get('cname')
		company=model.Company.get_by_id(int(cname))
		comments=model.Comment.query(model.Comment.file_info==uploadfile.key).order(-model.Comment.date)
		self.render_template('comment.html',users=users,company=company,key_comments=comments,uploadfile=uploadfile,member=member)
	
	def post(self):
		commenttext=self.request.POST.get('comment')
		commenter=self.request.POST.get('commenter')
		companyname=self.request.POST.get('companyname')
		company=self.request.POST.get('company')
		companykey=model.Company.get_by_id(int(company))
		fileid=self.request.POST.get('fileid')
		file = model.Uploadfiles.get_by_id(int(fileid))
		memberid=self.request.POST.get('memberid')
		mem = model.Member.get_by_id(int(memberid))
		
		usercomment=model.Comment(name=commenter,comment=commenttext,file_info=file.key,mem_key=mem.key,company=companykey.key)
		usercomment.put()
		self.redirect('/comment?filekey='+fileid+'&cname='+company)

		
		
class ImageUpHandler(basehandler.BaseHandler):
	@login_required
	def get(self):
		user=users.get_current_user()
		email=user.email()
		member=model.Member.query(model.Member.email==email).get() #for perticular user's data
		studentinfo=model.StudentInfo.query().fetch()
		for student in studentinfo:
			if email == student.email:
				#self.abort(403)
				#self.render_template('completedetail.html',users=users)
				self.redirect('/completedetail')
		if member:
			upload_url=blobstore.create_upload_url('/uploadimage')
			self.render_template('brochure.html',
								 users=users,
								 url=upload_url,member=member)
		else:
			self.abort(403)
			
class UnauthorizedHandler(basehandler.BaseHandler):	
	def get(self):
		self.render_template('unauthorized.html',users=users)

class BrochureHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		#email=users.get_current_user()
		user=users.get_current_user()
		email=user.email()
		member=model.Member.query(model.Member.email==email).get()
		studentinfo=model.StudentInfo.query().fetch()
		for student in studentinfo:
			if email == student.email:
				self.abort(403)
				#self.render_template('completedetail.html',users=users)
			
		name=self.request.POST.get('name')
		email=self.request.POST.get('email')
		division=self.request.POST.get('division')
		phoneno=self.request.POST.get('phoneno')
		tenth=self.request.POST.get('tenth')
		twelth=self.request.POST.get('twelth')
		grad=self.request.POST.get('grad')
		pgrad=self.request.POST.get('pgrad')
		proj1=self.request.POST.get('proj1')
		proj2=self.request.POST.get('proj2')
		proj3=self.request.POST.get('proj3')
		upload_files=self.get_uploads('filename')
		blob_info=upload_files[0]
		filename=self.request.POST["filename"].filename
		'''filename = Photo.get_by_id(int(self.request.get("filename")))
		img = images.Image(filename.blob_info)
		thumbnail = img.execute_transforms(output_encoding=images.png)
		self.response.headers['Content-Type'] = 'image/png'''
		#urllib.urlretrieve('self.request.POST["filename"]', 'E:\pd15\images')
		#filename1 = fig.savefig(os.path.join('E:\pd15\images','filename'))
		if '.jpg' or '.bmp' or '.png' or '.gif' in filename:
			user=model.StudentInfo(name=name,email=email,phoneno=phoneno,division=division,tenth=tenth,twelth=twelth,grad=grad,pgrad=pgrad,filename=filename,file_key=blob_info.key(),proj1=proj1,proj2=proj2,proj3=proj3)
			user.put()
			self.redirect('/')
		else:
			self.abort(403)
			#self.render_template('completedetail.html',users=users)
			
class BrochuredisplayHandler(basehandler.BaseHandler):
	@login_required
	def get(self):
		user=users.get_current_user()
		email=user.email()
		member=model.Member.query(model.Member.email==email).get()
		studentinfo=model.StudentInfo.query().fetch()
		if studentinfo:
			self.render_template('brochuredisplay.html',studentinfo=studentinfo,users=users)
		else:
			self.abort(403)
			#self.render_template('completedetail.html',users=users)
	
			
class CommentEditHandler(basehandler.BaseHandler):
	def get(self):
		fileid=self.request.get('fileid')
		file = model.Uploadfiles.get_by_id(int(fileid))
		company=self.request.get('company')
		member=self.request.get('member')
		commenter=self.request.get('commenter')
		commenttext=self.request.get('commenttext')
		comments = model.Comment.query(model.Comment.file_info==file.key).order(-model.Comment.date)
		self.render_template('edit1.html',users=users,file=file,company=company,member=member,commenter=commenter,commenttext=commenttext,key_comments=comments)
	
	def post(self):
		user=users.get_current_user()
		if user is None:
			self.abort(403)	
		commentid=self.request.POST.get('cid')
		commentkey = model.Comment.get_by_id(int(commentid))
		commenter=commentkey.name
		commenttext=commentkey.comment
		fileid=self.request.POST.get('file_id')
		filekey = model.Uploadfiles.get_by_id(int(fileid))
		company=self.request.POST.get('company')
		member=self.request.POST.get('memberid')
		commentkey.key.delete()
		self.redirect('/edit?commenter='+commenter+'&commenttext='+commenttext+'&fileid='+fileid+'&company='+company+'&member='+member)
		
		
class CommentDeleteHandler(basehandler.BaseHandler):
	def post(self):
		user=users.get_current_user()
		if user is None:
			self.abort(403)	
		commentid=self.request.POST.get('cid')
		commentkey = model.Comment.get_by_id(int(commentid))
		commenter=commentkey.name
		commenttext=commentkey.comment
		fileid=self.request.POST.get('file_id')
		filekey = model.Uploadfiles.get_by_id(int(fileid))
		company=self.request.POST.get('company')
		member=self.request.POST.get('memberid')
		commentkey.key.delete()
		self.redirect('/comment?filekey='+fileid+'&cname='+company)

class ContactHandler(basehandler.BaseHandler):
    def get(self):
        self.render_template('contact.html',users=users)

class AboutusHandler(basehandler.BaseHandler):
    def get(self):
        self.render_template('about.html',users=users)

class EditprofileHandler(basehandler.BaseHandler):
	def get(self):
		user=users.get_current_user()
		email=user.email()
		member=model.Member.query(model.Member.email==email).get()
		self.render_template("editprofile.html",users=users,member=member)

class UpdateprofileHandler(basehandler.BaseHandler):
	def get(self):
		user=users.get_current_user()
		email=user.email()
		member=model.Member.query(model.Member.email==email).get()
		self.render_template("updateprofile.html",users=users,member=member)
		
	def post(self):
		name=self.request.POST.get('name')
		email=self.request.POST.get('email')
		emails=['pramodmahapude@gmail.com','jain.mayu333@gmail.com']
		member=model.Member.query(model.Member.email==email).get()
		if email in emails:
			self.abort(403)
		if email in emails:
			type='a'
		else:
			type='u'
			
		phoneno=self.request.POST.get('phoneno')
		division=self.request.POST.get('division')
		member=self.request.POST.get('memberid')
		members = model.Member.get_by_id(int(member))
		user=model.Member(name=name,email=email,phoneno=phoneno,type=type,division=division)
		members.key.delete()
		user.put()
		self.redirect('/')
	

class CompleteDetailsHandler(basehandler.BaseHandler):
    def get(self):
        self.render_template('completedetail.html',users=users)
	
