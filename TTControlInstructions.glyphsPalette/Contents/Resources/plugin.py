# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Palette Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class ControlInstructions (PalettePlugin):
	dialogName = "com.mekkablue.ControlInstructionsPalette"
	dialog = objc.IBOutlet()
	controlInstructionsField = objc.IBOutlet()
	instanceLabel = objc.IBOutlet()
	
	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
			'en': u'TT Control Instructions',
			'de': u'TT-Kontrollinstruktionen'
		})
		
		self.min = 100
		self.max = 1000
		
		# Load .nib dialog (without .extension)
		self.loadNib('IBdialog', __file__)
	
	@objc.python_method
	def start(self):
		# Adding a callback for the 'GSUpdateInterface' event
		Glyphs.addCallback(self.update, UPDATEINTERFACE)
	
	@objc.python_method
	def __del__(self):
		Glyphs.removeCallback(self.update)

	@objc.IBAction
	def setInstructions_(self, sender):
		windowController = self.windowController()
		if windowController:
			thisFont = windowController.document().font
			if thisFont and thisFont.currentTab:
				currentInstance = thisFont.currentTab.previewInstances
				if type(currentInstance) != str:
					currentInstance.customParameters["TTFAutohint control instructions"] = self.controlInstructionsField.stringValue()

	@objc.python_method
	def update( self, sender ):
		if self.windowController():
			thisFont = self.windowController().document().font
			if thisFont and thisFont.currentTab:
				currentInstance = None
				try:
					currentInstance = thisFont.currentTab.previewInstances
				except Exception as e:
					print(e)
				if currentInstance and type(currentInstance) != str:
					self.instanceLabel.setStringValue_(currentInstance.name)
					controlInstructions = currentInstance.customParameters["TTFAutohint control instructions"]
					if controlInstructions:
						if controlInstructions[-1] != "\n":
							controlInstructions+="\n"
						self.controlInstructionsField.setStringValue_(controlInstructions)
					else:
						self.controlInstructionsField.setStringValue_("\n")
				else:
					self.instanceLabel.setStringValue_("Please select an instance")
					self.controlInstructionsField.setStringValue_("")

	def currentHeight(self):
		return Glyphs.intDefaults["com.mekkablue.ControlInstructionsPalette.height"]
	
	def setCurrentHeight_(self, newHeight):
		Glyphs.intDefaults["com.mekkablue.ControlInstructionsPalette.height"] = newHeight

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

	# def setSortID_(self, id):
	# 	pass
	# def sortID(self):
	# 	return 0