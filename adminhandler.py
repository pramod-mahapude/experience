import webapp2
import basehandler
from google.appengine.api import users
import model
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import mail
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import urllib
import authhelp
import authhelper

class CompanyEntryHandler(basehandler.BaseHandler):
	@login_required
	def get(self):
		user=users.get_current_user()
		self.render_template("companyentryone.html",users=users)

class CompanyHandler(basehandler.BaseHandler):
	@login_required
	def get(self):
		user=users.get_current_user()
		criteria=self.request.GET.get('criteria')
		if authhelp.auth_admin(user) == False:
			self.abort(403)
			return
		if "Yes" in criteria:
			self.render_template("companyentrytwo.html",users=users,criteria=criteria)
		else:
			self.render_template("companyentry.html",users=users,criteria=criteria)
			
		#self.render_template('companydetails.html',users=users)
        
	def post(self):
		user=users.get_current_user()
		criteria=self.request.POST.get('criteria')
		if authhelp.auth_admin(user) == False:
			self.abort(403)
			return
			
		cname=self.request.POST.get('cname')
		criteria=self.request.POST.get('criteria')
		stipend=self.request.POST.get('stipend')
		noofselectedcandidates=self.request.POST.get('noofselectedcandidates')			
		noofrounds=self.request.POST.get('noofrounds')
		tenth=self.request.POST.get('tenth')
		twelth=self.request.POST.get('twelth')
		grad=self.request.POST.get('grad')
		pgrad=self.request.POST.get('pgrad')
		company=model.Company(companyname=cname,criteria=criteria,stipend=stipend,noofselectedcandidates=noofselectedcandidates,noofrounds=noofrounds,tenth=tenth,twelth=twelth,grad=grad,pgrad=pgrad)
		company.put()
		self.redirect('/companyentryone')
		
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
			
class ReportdisplayHandler(basehandler.BaseHandler):
	@login_required
	def get(self):
		user=users.get_current_user()
		members=model.Member.query().count()
		comments=model.Comment.query().count()
		files=model.Uploadfiles.query().count()
		companies=model.Company.query().count()
		
		self.render_template('reports.html',users=users,members=members,comments=comments,files=files,companies=companies)
		
class FiledisplayHandler(basehandler.BaseHandler):
	@login_required
	def get(self):
		fileinfo=model.Uploadfiles.query().fetch()
		if fileinfo:
			self.render_template('adminfiledisplay.html',fileinfo=fileinfo,users=users)
		else:
			self.abort(403)
		
			
		
class FileUpHandler(basehandler.BaseHandler):
	@login_required
	def get(self):
		cnames=model.Company.query()
		upload_url=blobstore.create_upload_url('/adminupload')
		self.render_template('adminuploadfile.html',cnames=cnames,
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
		company=model.Company.get_by_id(int(companyname))
		uploadfiles=model.Uploadfiles(filename=filename,company=company.key,name=member.name,file_key=blob_info.key())
		uploadfiles.put();
		self.redirect('/adminindex')
		
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
		self.render_template('admincomment.html',users=users,company=company,key_comments=comments,uploadfile=uploadfile,member=member)
	
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
		self.redirect('/admincomment?filekey='+fileid+'&cname='+company)
		
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
		self.redirect('/admincomment?filekey='+fileid+'&cname='+company)