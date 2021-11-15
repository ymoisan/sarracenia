#!/usr/bin/python3
"""
  msg_total

  give a running total of the messages going through an exchange.
  as this is an on_msg

  accumulate the number of messages and the bytes they represent over a period of time.
  options:

  msg_total_interval -- how often the total is updated. (default: 5)
  msg_total_maxlag  -- if the message flow indicates that messages are 'late', emit warnings.
                    (default 60)

  dependency:
     requires python3-humanize module.

"""

import os, stat, time
from sarracenia.flowcb import FlowCB
import calendar
import humanize
import datetime
import logger
from sarracenia import timestr2flt, timeflt2str, nowflt

logger = logging.getLogger(__name__)


class Msg_Total(FlowCB):
    def __init__(self, options):
        """
           set defaults for options.  can be overridden in config file.
        """
        self.o = options

        # make self.o know about these possible options

        self.o.declare_option('msg_total_interval')
        self.o.declare_option('msg_total_maxlag')

        if hasattr(self.o, 'msg_total_maxlag'):
            if type(self.o.msg_total_maxlag) is list:
                self.o.msg_total_maxlag = int(self.o.msg_total_maxlag[0])
        else:
            self.o.msg_total_maxlag = 60

        if hasattr(self.o, 'msg_total_interval'):
            if type(self.o.msg_total_interval) is list:
                self.o.msg_total_interval = int(self.o.msg_total_interval[0])
        else:
            self.o.msg_total_interval = 5

        now = nowflt()

        self.o.msg_total_last = now
        self.o.msg_total_start = now
        self.o.msg_total_msgcount = 0
        self.o.msg_total_bytecount = 0
        self.o.msg_total_lag = 0
        logger.debug("msg_total: initialized, interval=%d, maxlag=%d" % \
                     (self.o.msg_total_interval, self.o.msg_total_maxlag))

        self.o.msg_total_cache_file = self.o.user_cache_dir + os.sep
        self.o.msg_total_cache_file += 'msg_total_plugin_%.4d.vars' % self.o.instance

    def on_message(self):
        msg = self.o.msg

        if msg['isRetry']: return True

        if (self.o.msg_total_msgcount == 0):
            logger.info("msg_total: 0 messages received: 0 msg/s, 0.0 bytes/s, lag: 0.0 s (RESET)")

        msgtime = timestr2flt(msg['pubtime'])
        now = nowflt()

        self.o.msg_total_msgcount = self.o.msg_total_msgcount + 1

        lag = now - msgtime
        self.o.msg_total_lag = self.o.msg_total_lag + lag

        # message with sum 'R' and 'L' have no partstr
        if hasattr(self.o.msg, 'partstr'):
            (method, psize, ptot, prem, pno) = msg['partstr'].split(',')
            self.o.msg_total_bytecount = self.o.msg_total_bytecount + int(psize)

        # not time to report yet.
        if self.o.msg_total_interval > now - self.o.msg_total_last:
            return True

        logger.info("msg_total: %3d messages received: %5.2g msg/s, %s bytes/s, lag: %4.2g s" %
                    (self.o.msg_total_msgcount, self.o.msg_total_msgcount /
                     (now - self.o.msg_total_start),
                     humanize.naturalsize(
                         self.o.msg_total_bytecount / (now - self.o.msg_total_start),
                         binary=True,
                         gnu=True), self.o.msg_total_lag / self.o.msg_total_msgcount))
        # Set the maximum age, in seconds, of a message to retrieve.

        if lag > self.o.msg_total_maxlag:
            logger.warning("total: Excessive lag! Messages posted %s " %
                           humanize.naturaltime(datetime.timedelta(seconds=lag)))

        self.o.msg_total_last = now
        return True

    # restoring accounting variables
    def on_start(self):

        self.o.msg_total_cache_file = self.o.user_cache_dir + os.sep
        self.o.msg_total_cache_file += 'msg_total_plugin_%.4d.vars' % self.o.instance

        if not os.path.isfile(self.o.msg_total_cache_file): return True

        fp = open(self.o.msg_total_cache_file, 'r')
        line = fp.read(8192)
        fp.close()

        line = line.strip('\n')
        words = line.split()
        if len(words) > 4:
            self.o.msg_total_last = float(words[0])
            self.o.msg_total_start = float(words[1])
            self.o.msg_total_msgcount = int(words[2])
            self.o.msg_total_bytecount = int(words[3])
            self.o.msg_total_lag = float(words[4])
        else:
            logger.error("missing cached variables in file: {}".format(self.o.post_total_cache_file))
            return False
        return True

    # saving accounting variables
    def on_stop(self, options):

        line = '%f ' % self.o.msg_total_last
        line += '%f ' % self.o.msg_total_start
        line += '%d ' % self.o.msg_total_msgcount
        line += '%d ' % self.o.msg_total_bytecount
        line += '%f\n' % self.o.msg_total_lag

        fp = open(self.o.msg_total_cache_file, 'w')
        fp.write(line)
        fp.close()
        return True


