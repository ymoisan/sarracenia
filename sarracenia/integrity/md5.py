from hashlib import md5

from sarracenia.integrity import Integrity


class Md5(Integrity):
    """
         use the (obsolete) Message Digest 5 (MD5) algorithm, applied on the content
         of a file, to generate an integrity signature.
      """

    @staticmethod
    def registered_as():
        """
            v2name.
          """
        return 'd'

    def set_path(self, path):
        self.filehash = md5()

    def update(self, chunk):
        if type(chunk) == bytes: self.filehash.update(chunk)
        else: self.filehash.update(bytes(chunk, 'utf-8'))
