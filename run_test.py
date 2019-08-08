# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 12:49
# @Author  : Tao.Xu
# @Email   : tao.xu2008@outlook.com

"""
Test suites run
"""

import os
import sys
import argparse
import unittest
from tlib.stressrunner import StressRunner
from tlib import log

LOG_PATH = os.path.join(os.getcwd(), 'log')
LOGFILE_PATH = os.path.join(LOG_PATH, 'run_test.log')
my_logger = log.get_logger(logfile=LOGFILE_PATH, logger_name='test', debug=True, reset_logger=True)


def parse_arg():
    """
    Set argument
    :return:
    """

    # Parent parser
    parser = argparse.ArgumentParser(description='Panzura Vizion Test Project')
    parser.add_argument("--debug", action="store_true", dest="debug", default=False,
                        help="debug mode,will not send email")
    parser.add_argument("--run_time", action="store", dest="run_time", default=60*60*24*3, type=int,
                        help="run time(s),default:60*60*24*3 (3 days)")
    parser.add_argument("--run_iteration", action="store", dest="run_iteration", default=0, type=int,
                        help="run_iteration(0:keep run forever),default:0")
    parser.add_argument("--sys_user", action="store", dest="sys_user", default="root", help="system user")
    parser.add_argument("--sys_pwd", action="store", dest="sys_pwd", default="password", help="system password")
    parser.add_argument("--key_file", action="store", dest="key_file", default=None, help="system login key_file")
    parser.add_argument("-m", action="store", dest="comment", default=None, help="test comment")
    parser.add_argument("--mail_to", action="store", dest="mail_to", default=None, help="mail_to, split with ';'")
    parser.set_defaults(runner='StressRunner', project='ut')
    # Sub parser
    subparsers = parser.add_subparsers(help='project: unit test')

    # ----------------- cc sub-commands -----------------
    # test_parser = subparsers.add_parser('test', help='sub command of test')
    # test_parser.set_defaults(project='test')
    #
    # subparsers = test_parser.add_subparsers(help='unit test')
    from test.argument import set_subparsers_suite
    set_subparsers_suite(subparsers)

    return parser.parse_args()


def main_1():
    """Main method
    """
    args = parse_arg()
    command = 'python ' + ' '.join(sys.argv)

    my_logger.info('Test args:\n{0}'.format(args))
    my_logger.info("Test command:\n{cmd}".format(cmd=command))

    # -----------------------------
    # --- Run unittest suite
    # -----------------------------
    if args.runner == 'TextTestRunner':
        # run with TextTestRunner
        from unittest import TextTestRunner
        runner = TextTestRunner(verbosity=2)
    else:
        # run with StressRunner -- report html
        # run with StressRunner -- report html
        runner = StressRunner(
            report_path=LOG_PATH,
            report_name='run_test_report.html',
            title='My unit test',
            description='This demonstrates the report output by StressRunner.',
            logger=my_logger
        )

    # get unittest test suite and then run unittest case
    test_suite = args.func(args)
    runner.run(test_suite)

    return True


def main_2():
    from test.test_log import TestLog
    from test.test_mail import TestMail

    # Generate test suite
    # test_suite = unittest.TestSuite(map(TestLog, ['test_1']))
    test_suite = unittest.TestSuite()
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLog))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMail))

    # output to a file
    runner = StressRunner(
        report_path=LOG_PATH,
        title='My unit test',
        description='This demonstrates the report output by StressRunner.',
        logger=my_logger
    )
    runner.run(test_suite)


if __name__ == '__main__':
    main_1()
