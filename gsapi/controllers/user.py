from model import Mod
from schematics.models import Model as _Model
from schematics.types import IntType, StringType, FloatType, DateTimeType, EmailType, URLType
from schematics.types.compound import ListType, ModelType

from schematics.types.mongo import ObjectIdType
from bson import ObjectId
from embed import Email, Note, Phone, Im
from place import PlaceRel
from contact import Usr

class Usr(self):
	def add_user(self, user):
		verify username is not empty
		query db for username availability using ajax
		if not available show it
		verify password for strength using client side validation
		if not strong enough do not allow to create login
		generate sha-256 hash of password
		store both password and username
		get first name and last name and verify both are not empty
		get email and verify that it is not already in use using ajax
		other details are optional
		if user does not provide an image generate one using gravatar
		else use that image
		store all the information in database
		generate validation token, store it in database with expiry time
		send validation/welcome email with validation link using validation token

	def validate_user(self, validation_token):
		get validation token from GET request
		query db for existence of token

		if found check token for expiry time
			if token has not expired mark user valid
			else display a message saying token has expired

		else display a message saying email is not registered with the application

	def reset_password(self, rstTkn):
		''' When user clicks link sent by email for resetting password. '''

		check for avalability and expiry in database
		if available and not expired
			provide reset password form
			get and validate input
			generate password hash and store it
		else
			if token has expired
				display a message that token has expired
			else
				display a message that token was not found

	def reset_password_req(self, email):
		''' If user forgets his password and wants to reset password. '''
		get email from form
		check if email is well formed
		search email
		if found
			generate reset token and store in db with expiry time
			send email to provided email address along with reset token
		else
			display a message saying email not found in database

	def user_id_req(self, email):
		''' In case user forgets his id '''

		get email from form
		check if email is well formed
		search email
		if found
			get user id from database and send by email
		else
			display a message saying email not found in database

	def edit_profile(self, user):
		''' If user wants to edit his profile. '''

		check if user has a session
		if seesion found
			fetch all data from database for that user id
			display in form
			when form is submitted
			if email is different
				send validation email persist data temporarily
				on validation of email validate and store
				send notification email for profile changes
			else
				validate and store
		else
			display a message saying session invalid

	def change_password(self, user):
		present form for password change
		validate and store hash
		send password change notificatrion

	def delete_profile(self, user):
		mark user inactive

	def search_user(self, user):
		search for user based on particular parameter
		if user if not inactive show profile

	def invite_user(self, email):
		check email for validity
		send an invitation email to that email with a link to create a login

	def login(self, credentials):
		check user_id in database
		if found
			generate hash of supplied
			compare password generated hash with database password hash
			if match is found
				set seeion/cookie and persent user home page
			else
				display a message saying user_id or password is incorrect
		else
			display a message saying user_id or password is incorrect

	def logout(self, user):
		unset session/cookie and present with site home page
