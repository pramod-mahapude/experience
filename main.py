#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import basehandler
from google.appengine.api import users
import model

class MainHandler(basehandler.BaseHandler):
    def get(self):
        self.render_template('index.html',users=users)
        
	

 
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/register',handler='userhandler.RegisterHandler'),
	webapp2.Route('/login',handler='userhandler.LoginHandler'),
	webapp2.Route('/unauthorized', handler='userhandler.UnauthorizedHandler'),
	webapp2.Route('/index',handler='userhandler.GeneralHandler'),
	webapp2.Route('/memdisplay',handler='userhandler.MemdisplayHandler'),
	webapp2.Route('/companydetails',handler='adminhandler.CompanyHandler'),
	webapp2.Route('/fileup',handler='userhandler.FileUpHandler'),
	webapp2.Route('/upload',handler='userhandler.UploadHandler'),
	webapp2.Route('/filedisplay',handler='userhandler.FiledisplayHandler'),
	webapp2.Route('/download',handler='userhandler.DownloadHandler'),
	webapp2.Route('/companyentry',handler='adminhandler.CompanyHandler'),
	webapp2.Route('/companynotice',handler='adminhandler.CompanynoticeHandler'),
	webapp2.Route('/brochure',handler='userhandler.ImageUpHandler'),
	webapp2.Route('/uploadimage',handler='userhandler.BrochureHandler'),
	webapp2.Route('/contact',handler='userhandler.ContactHandler'),
	webapp2.Route('/about',handler='userhandler.AboutusHandler'),
	webapp2.Route('/adminindex',handler='userhandler.AdminIndexHandler'),
	webapp2.Route('/companyentryone',handler='adminhandler.CompanyEntryHandler'),
	webapp2.Route('/comment',handler='userhandler.CommentHandler'),
	webapp2.Route('/edit',handler='userhandler.CommentEditHandler'),
	webapp2.Route('/delete',handler='userhandler.CommentDeleteHandler'),
	webapp2.Route('/brochuredisplay',handler='adminhandler.BrochuredisplayHandler'),
	webapp2.Route('/completedetail',handler='userhandler.CompleteDetailsHandler'),
	webapp2.Route('/editprofile',handler='userhandler.EditprofileHandler'),
	webapp2.Route('/reports',handler='adminhandler.ReportdisplayHandler'),
	webapp2.Route('/adminfileup',handler='adminhandler.FileUpHandler'),
	webapp2.Route('/adminfiledisplay',handler='adminhandler.FiledisplayHandler'),
	webapp2.Route('/adminupload',handler='adminhandler.UploadHandler'),
	webapp2.Route('/admindownload',handler='adminhandler.DownloadHandler'),
	webapp2.Route('/admincomment',handler='adminhandler.CommentHandler'),
	webapp2.Route('/adminedit',handler='adminhandler.CommentEditHandler'),
	webapp2.Route('/admindelete',handler='adminhandler.CommentDeleteHandler'),
	webapp2.Route('/updateprofile',handler='userhandler.UpdateprofileHandler'),
	
], debug=True, config=basehandler.config)