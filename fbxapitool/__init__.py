#-*- coding:utf-8 -*-

'''
Provides authentification and row access to Freebox using Freebox OS developper API.
Freebox API documentation : http://dev.freebox.fr/sdk/os/ or http://mafreebox.freebox.fr/doc/index.html#
'''

__version__ = '8.1.0'
__all__ = ['fbxapitool']

from fbxapitool.fbxapitool import Freebox
