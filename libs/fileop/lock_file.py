# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 12:49
# @Author  : Tao.Xu
# @Email   : tao.xu2008@outlook.com

"""
:description:
    file related functions
"""
import os
import sys
import fcntl

from libs import err
from libs import decorators


__all__ = [
    'LockFile', 'FILELOCK_SHARED', 'FILELOCK_EXCLUSIVE',
    'FILELOCK_NONBLOCKING', 'FILELOCK_UNLOCK'
]


FILELOCK_EXCLUSIVE = fcntl.LOCK_EX
FILELOCK_SHARED = fcntl.LOCK_SH
FILELOCK_NONBLOCKING = fcntl.LOCK_NB
FILELOCK_UNLOCK = fcntl.LOCK_UN


class LockFile(object):
    """
    lock file class
    """

    def __init__(self, fpath, locktype=FILELOCK_EXCLUSIVE):
        """
        exclusive lockfile, by default.

        Notice that the file CANNOT exist before you intialize a LockFile obj.
        Otherwise, it will raise tlib.err.LockFileError

        :raise:
            tlib.err.LockFileError if we encounter errors
        """
        self._fpath = fpath
        self._locktype = locktype
        self._fhandle = None
        try:
            # if FILELOCK_EXCLUSIVE == locktype:
            #     self._fhandle = os.open(
            #         self._fpath, os.O_CREAT|os.O_EXCL|os.O_RDWR
            #     )
            # else:
            self._fhandle = os.open(
                self._fpath, os.O_CREAT | os.O_RDWR
            )
        except IOError as error:
            raise err.LockFileError(error)
        except Exception as error:
            raise err.LockFileError(
                'catch unkown error type:{0}'.format(error)
            )

    def __del__(self):
        """del the instance"""
        try:
            if self._fhandle is not None:
                os.close(self._fhandle)
        except Exception as error:
            sys.stderr.write('failed to close lockfile:{0}, msg:{1}'.format(
                self._fpath, error)
            )
            sys.stderr.flush()

    @decorators.needposix
    def lock(self, blocking=True):
        """
        lock the file

        :param blocking:
            If blocking is True, will block there until tlib gets the lock.
            True by default.

        :return:
            return False if locking fails

        :raise Exception:
            raise tlib.err.LockFileError if blocking is False and
            the lock action failed
        """
        flags = 0x1
        if FILELOCK_SHARED == self._locktype:
            flags = FILELOCK_SHARED
        elif FILELOCK_EXCLUSIVE == self._locktype:
            flags = FILELOCK_EXCLUSIVE
        else:
            raise err.LockFileError('does not support this lock type')
        if not blocking:
            flags |= FILELOCK_NONBLOCKING
        ret = None
        try:
            ret = fcntl.flock(self._fhandle, flags)
        except IOError as error:
            raise err.LockFileError(error)
        except Exception as error:
            raise err.LockFileError(error)
        return ret

    def unlock(self):
        """unlock the locked file"""
        try:
            fcntl.flock(self._fhandle, FILELOCK_UNLOCK)
        except Exception as error:
            raise err.LockFileError(error)
