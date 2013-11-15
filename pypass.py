#!/usr/bin/env python


'''Asks for two words, puts them together and creates a md5 password. All you have to do is remember a name, place or date and type in the site.'''
__author__ = "sk5 <eric@godta.com>"
__desc__ = 'Asks for two words, puts them together and creates a md5 password. All you have to do is remember a name, place or date and type in the site.'
__prog__ = 'PyPass [Python Password Creator]'
__version__ = '0.1'

SUPPORTED_VERSIONS = [(2, 6),(2, 7)]

import  os, re, sys, string
from Tkinter import Tk
from hashlib import md5 as m

class bcolors:
	'''Pretty Colors Oooooh!'''
	YELLOW = '\033[93m'
	RED = '\033[91m'
	GREY = '\033[0m'
	CYAN = '\033[96m'
	DCYAN = '\033[36m'
	DBLUE = '\033[34m'
	BLACK = '\033[90m'
	WHITE = '\033[97m'

	def disable(self):
		'''Resets all colors'''
		self.YELLOW = ''
		self.RED = ''
		self.GREY = ''
		self.CYAN = ''
		self.DCYAN = ''
		self.DBLUE = ''
		self.BLACK = ''
		self.WHITE = ''


# Pyperclip v1.3
# A cross-platform clipboard module for Python. (only handles plain text for now)
# By Al Sweigart al@coffeeghost.net

# Usage:
#   import pyperclip
#   pyperclip.copy('The text to be copied to the clipboard.')
#   spam = pyperclip.paste()

# On Mac, this module makes use of the pbcopy and pbpaste commands, which should come with the os.
# On Linux, this module makes use of the xclip command, which should come with the os. Otherwise run "sudo apt-get install xclip"


# Copyright (c) 2010, Albert Sweigart
# All rights reserved.
#
# BSD-style license:
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the pyperclip nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Albert Sweigart "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Albert Sweigart BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Change Log:
# 1.2 Use the platform module to help determine OS.
# 1.3 Changed ctypes.windll.user32.OpenClipboard(None) to ctypes.windll.user32.OpenClipboard(0), after some people ran into some TypeError

import platform, os

def winGetClipboard():
    ctypes.windll.user32.OpenClipboard(0)
    pcontents = ctypes.windll.user32.GetClipboardData(1) # 1 is CF_TEXT
    data = ctypes.c_char_p(pcontents).value
    #ctypes.windll.kernel32.GlobalUnlock(pcontents)
    ctypes.windll.user32.CloseClipboard()
    return data

def winSetClipboard(text):
    GMEM_DDESHARE = 0x2000
    ctypes.windll.user32.OpenClipboard(0)
    ctypes.windll.user32.EmptyClipboard()
    try:
        # works on Python 2 (bytes() only takes one argument)
        hCd = ctypes.windll.kernel32.GlobalAlloc(GMEM_DDESHARE, len(bytes(text))+1)
    except TypeError:
        # works on Python 3 (bytes() requires an encoding)
        hCd = ctypes.windll.kernel32.GlobalAlloc(GMEM_DDESHARE, len(bytes(text, 'ascii'))+1)
    pchData = ctypes.windll.kernel32.GlobalLock(hCd)
    try:
        # works on Python 2 (bytes() only takes one argument)
        ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData), bytes(text))
    except TypeError:
        # works on Python 3 (bytes() requires an encoding)
        ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData), bytes(text, 'ascii'))
    ctypes.windll.kernel32.GlobalUnlock(hCd)
    ctypes.windll.user32.SetClipboardData(1,hCd)
    ctypes.windll.user32.CloseClipboard()

def macSetClipboard(text):
    outf = os.popen('pbcopy', 'w')
    outf.write(text)
    outf.close()

def macGetClipboard():
    outf = os.popen('pbpaste', 'r')
    content = outf.read()
    outf.close()
    return content

def gtkGetClipboard():
    return gtk.Clipboard().wait_for_text()

def gtkSetClipboard(text):
    cb = gtk.Clipboard()
    cb.set_text(text)
    cb.store()

def qtGetClipboard():
    return str(cb.text())

def qtSetClipboard(text):
    cb.setText(text)

def xclipSetClipboard(text):
    outf = os.popen('xclip -selection c', 'w')
    outf.write(text)
    outf.close()

def xclipGetClipboard():
    outf = os.popen('xclip -selection c -o', 'r')
    content = outf.read()
    outf.close()
    return content

def xselSetClipboard(text):
    outf = os.popen('xsel -i', 'w')
    outf.write(text)
    outf.close()

def xselGetClipboard():
    outf = os.popen('xsel -o', 'r')
    content = outf.read()
    outf.close()
    return content


if os.name == 'nt' or platform.system() == 'Windows':
    import ctypes
    getcb = winGetClipboard
    setcb = winSetClipboard
elif os.name == 'mac' or platform.system() == 'Darwin':
    getcb = macGetClipboard
    setcb = macSetClipboard
elif os.name == 'posix' or platform.system() == 'Linux':
    xclipExists = os.system('which xclip') == 0
    if xclipExists:
        getcb = xclipGetClipboard
        setcb = xclipSetClipboard
    else:
        xselExists = os.system('which xsel') == 0
        if xselExists:
            getcb = xselGetClipboard
            setcb = xselSetClipboard
        try:
            import gtk
            getcb = gtkGetClipboard
            setcb = gtkSetClipboard
        except:
            try:
                import PyQt4.QtCore
                import PyQt4.QtGui
                app = QApplication([])
                cb = PyQt4.QtGui.QApplication.clipboard()
                getcb = qtGetClipboard
                setcb = qtSetClipboard
            except:
                raise Exception('Pyperclip requires the gtk or PyQt4 module installed, or the xclip command.')
copyClip = setcb
pasteClip = getcb


def clear():
	'''uhm... this clears the screen ...'''
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')
	return 0

def run():
	'''Runs the Python Password Creator Program.  No arguments are required'''

	rows, columns = os.popen('stty size', 'r').read().split()
	TYPE = 0
	clear()
	print
	print(bcolors.CYAN)
	header = bcolors.DCYAN+" -[ Python Password Creator v"+bcolors.CYAN+"0.1"+bcolors.DCYAN+" ]- "
	print(header.center(int(columns)+12))
	print

	Pass1 = raw_input(bcolors.DCYAN+'  Enter First Password '+bcolors.WHITE+': '+bcolors.CYAN)
	Pass2 = raw_input(bcolors.DCYAN+'  Now The Second       '+bcolors.WHITE+': '+bcolors.CYAN)
	while True:
		h = set(['1','2', 'q'])
		print
		print(bcolors.DCYAN+'  ['+bcolors.CYAN+'1'+bcolors.DCYAN+'] Hex Digest ('+bcolors.WHITE+'23fd44228071730e3457dc5de887b3ae'+bcolors.DCYAN+')')
		print(bcolors.DCYAN+'  ['+bcolors.CYAN+'2'+bcolors.DCYAN+'] Digest     ('+bcolors.WHITE+'#\xfdD"\x80qs\x0e4W\xdc]\xe8\x87\xb3\xae'.encode('string_escape')+bcolors.DCYAN+')')
		print
		TYPE = raw_input(bcolors.DCYAN+'  Type of Digest ['+bcolors.CYAN+'1'+bcolors.DCYAN+'-'+bcolors.CYAN+'2'+bcolors.DCYAN+', '+bcolors.WHITE+'Q'+bcolors.DCYAN+'] '+bcolors.WHITE+': '+bcolors.CYAN);
		if TYPE in h:
			break
		elif TYPE not in h:
			TYPE = 0

	if (string.lower(TYPE) == 'q'):
		print
		print(bcolors.RED+"  Program Terminated")
		print(bcolors.GREY)
		quit(0)
		
	elif (TYPE == '1'):
		md5_hash = m(Pass1+Pass2).hexdigest()
		s = bcolors.WHITE+md5_hash
		md = md5_hash
	else:
		md5_hash = m(Pass1+Pass2).digest()
		s = bcolors.WHITE+md5_hash.encode('string_escape')
		md = md5_hash.encode('string_escape')

	clear()
	copyClip(md) # copy to clipboard
	print
	print
	
	newpass = bcolors.CYAN+unichr(0x2212)+bcolors.DCYAN+'[ your new password is ]'+bcolors.CYAN+unichr(0x2212)
	clipboard = bcolors.CYAN+pasteClip()+bcolors.DCYAN+' has been copied to the clipboard!'
	
	print(newpass.center(int(columns)+10))
	print (bcolors.GREY)
	print(s.center( int(columns)-2 ) )
	print(bcolors.GREY)
	print(clipboard.center(int(columns)+10))
	print
	print

if (len(sys.argv) > 1):
	if (string.lower(sys.argv[1]) == 'run'):
		run()
else:
	print("Either import this,  or run '" + sys.argv[0] + " run' to start.")
	

