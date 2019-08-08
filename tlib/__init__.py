# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 12:49
# @Author  : Tao.Xu
# @Email   : tao.xu2008@outlook.com

"""
Some own/observed great lib/ideas,common useful python libs.
"""

import sys
import test
from tlib import log
from tlib import decorators
from tlib import err

# from tlib import mail
# from tlib import shell
# from tlib import net
from tlib import version
# from tlib import timeplus as time
# from tlib import timeplus
# from tlib import util
# from tlib import unittest
# from tlib import res
# from tlib.shell import oper
# from tlib import thirdp
from tlib import platforms

if sys.version_info < (2, 6):
    raise ImportError('tlib needs to be run on python 2.6 and above.')


# __all__ = [
#     'err', 'net', 'log', 'mail', 'shell', 'time',
#     'util', 'unittest', 'decorators', 'thirdp', 'platforms'
# ]
__all__ = [
    'err', 'log', 'decorators', 'platforms', 'shell', 'version'
]
