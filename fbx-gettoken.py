#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Use it to get the auth token once, all other usages of the package will then use this token
'''

from fbxapitool import Freebox
fbx = Freebox()
fbx.open('mafreebox.freebox.fr',443)
print('Token ready')
fbx.close()
