# coding: utf-8
# Access8Math: Allows access math content written by MathML in NVDA
# Copyright (C) 2018 Tseng Woody <tsengwoody.tw@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.

import globalPluginHandler
from logHandler import log

import characterProcessing
from characterProcessing import *

class CustomCharacterDescriptions(object):
	"""
	Represents a map of characters to one or more descriptions (examples) for that character.
	The data is loaded from a file from the requested locale.
	"""

	def __init__(self,locale):
		"""
		@param locale: The characterDescriptions.dic file will be found by using this locale.
		@type locale: string
		"""
		self._entries = {}
		fileName=os.path.join('locale',locale,'characterDescriptions.dic')
		if not os.path.isfile(fileName): 
			raise LookupError(fileName)
		f = codecs.open(fileName,"r","utf_8_sig",errors="replace")
		for line in f:
			if line.isspace() or line.startswith('#'):
				continue
			line=line.rstrip('\r\n')
			temp=line.split("\t")
			if len(temp) > 1:
				key=temp.pop(0)
				self._entries[key] = temp
			else:
				log.warning("can't parse line '%s'" % line)
		log.debug("Loaded %d entries." % len(self._entries))
		f.close()

		# custom character.dic
		fileName = os.path.join(globalVars.appArgs.configPath, "characterDescriptions-%s.dic" % locale)
		if not os.path.isfile(fileName):
			return
		f = codecs.open(fileName,"r","utf_8_sig",errors="replace")
		for line in f:
			if line.isspace() or line.startswith('#'):
				continue
			line=line.rstrip('\r\n')
			temp=line.split("\t")
			if len(temp) > 1:
				key=temp.pop(0)
				self._entries[key] = temp
			else:
				log.warning("can't parse line '%s'" % line)
		log.debug("Loaded %d entries." % len(self._entries))
		f.close()

	def getCharacterDescription(self, character):
		"""
		Looks up the given character and returns a list containing all the description strings found.
		"""
		return self._entries.get(character)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		characterProcessing._charDescLocaleDataMap=LocaleDataMap(CustomCharacterDescriptions)
		log.info('123')