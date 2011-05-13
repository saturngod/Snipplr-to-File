# -*- coding: utf-8 -*-

# SnipplrPy.py -- Snipplr Python Wrapper
#
# Copyright (C) 2007 - Francisco Jesús Jordano Jiménez <arcturus@ardeenelinfierno.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Some ideas and code taken from Avinash Vora (http://www.avinashv.net/) and
# his tool SnipplrCLI (http://www.avinashv.net/snipplrcli/)

import xmlrpclib
import os
import urllib2

__all__ = ('SnipplrPy',)
__author__ = "Francisco Jesús Jordano Jiménez"
__revision__ = 0.4

class SnipplrPy:
	"""
		Wrapper around xml-rpc methods exposed by
		Snipplr.
	"""
	
	def __init__(self):
		"""
			Constructor
		"""
		self.api_key = None
		self.server_url = "http://snipplr.com/xml-rpc.php"
		self.server = None
		self.initialized = False
		self.languages = {}
		
	def __try_connect__(self):
		"""
			Private method, try to connect with xml-rpc endpoint if
			still not connected
		"""
		if self.server is None:
			try:
				self.server = xmlrpclib.Server(self.server_url)
				return True
			except xmlrpclib.Fault:
				return False
		return True
		
	def check_api_key(self, key):
		"""
			Checks if the key suministrated is valid or not
		"""		
		if self.__try_connect__() == False:
			return False
		
		try:
			if self.server.user.checkkey(key) == 0:
				return False
			return True
		except xmlrpclib.Fault:
			return False
			
	def list_languages(self):
		"""
			List snipplr languages
		"""
		if len(self.languages.keys()) != 0:
			return self.languages
		
		if self.__try_connect__() == False:
			return None
			
		try:
			self.languages = self.server.languages.list()
			return self.languages
		except xmlrpclib.Fault:
			return None
			
	def setup(self, api_key):
		"""
			Setup the object with a valid api_key
		"""
		if self.check_api_key(api_key) == False:
			self.initialized = False
			return False;
		
		self.api_key = api_key
		self.initialized = True
		
		return True
		
	def get(self, id, parse_source = False):
		"""
			Get the snippet specified by id
			None if the id is not valid.
			We dont need the api key here.
			If parse_source is True, replace html html encoding with 
			the implicit value
		"""
		if self.__try_connect__() == False:
			return None
			
		try:
			result = self.server.snippet.get(id)
			if parse_source:
				self.__convert_snippet_source__(result)
			return result
		except xmlrpclib.Fault:
			return None
		
	def get_source_plain_text(self, id):
		"""
			Get the source code in plain
			text format
		"""
		
		url = "http://snipplr.com/view.php?id=" + str(id) + "&plaintext"
		
		try:
			handler = urllib2.urlopen(url)
			source = handler.read()
			handler.close()
			return source
		except Exception, e:
			return None			
			
	def list(self, tags = None, sort = None, limit = None):
		"""
			List the user snnipets.
			tags is a space separated string with the tags names.
			sort can be one of these three values: title, date, random. DEACTIVATED
			limit is the max number of snippet returned. DEACTIVATED
		"""
		if self.initialized == False:
			return None
			
		try:
			if tags == None:
				t = ""
			else:
				t = tags
			return self.server.snippet.list(self.api_key, t)
		except xmlrpclib.Fault:
			return None
			
	def post(self, title, code, tags = None, language = None):
		"""
			Post a new snippet. Returns True if proccess ok
			or False in other case
		"""
		
		if self.initialized == False:
			return False
		
		if language:
			if not language in self.list_languages():
				error_str = "Language not included into Snipplr language list " + " ".join(self.languages.keys())
				raise Exception(error_str)
				
		
		try:
			#Default values
			t = tags
			if t == None:
				t = ""
			l = language
			if l == None:
				l = ""
			self.server.snippet.post(self.api_key, title, code, t, l)
			return True 
		except xmlrpclib.Fault:
			return False
		
	def post_file(self, file, title, tags = None, language = None):
		"""
			Post a snippet taken the code from a file.
			Returns True if succedded, or False in other case
		"""
		if os.access(file, os.R_OK):
			handler = open(file, "r")
			code = handler.read()
			handler.close()
			
			return self.post(title, code, tags, language)
		
		return False
		
	def delete(self, id):
		"""
			Try to delete the snippet specified by id.
			Returns true if action is taken or false in other case
		"""
		if self.initialized == False:
			return False
			
		try:
			if self.server.snippet.delete(self.api_key, id) == 0:
				return False
			return True
		except xmlrpclib.Fault:
			return False
			
	def __convert_snippet_source__(self, snippet):
		"""
			Replace all  html chars with their implicit
			values
		"""
		#Yes i know this is actually soooo ugly and we should use regexp :P
		snippet["source"] = snippet["source"].replace("&quot;","\"").replace("&lt;","<").replace("&gt;",">")
		
		return snippet