import logging
import os

logger = logging.getLogger(__name__)


class DeleteFlowFiles(object):
    """
       This is a custom callback class for the sr_insects flow tests.
       delete files for messages in two directories.
    """
    def __init__(self, parent):
        logger.debug("msg_delete initialized")

    def after_accept(self, worklist):

        for m in worklist.incoming:

            f = "%s%s%s" % (m['new_dir'], os.sep, m['new_file'])
            logger.info("msg_delete: %s" % f)
            try:
                os.unlink(f)
                os.unlink(f.replace('/cfr/', '/cfile/'))
                worklist.ok.append(m)
            except OSError as err:
                logger.error("could not unlink {}: {}".format(f, err))
                logger.debug("Exception details:", exc_info=True)
                worklist.failed.append(m)
        worklist.incoming = []
