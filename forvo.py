# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2014 Roland Sieker, ospalh@gmail.com
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

# For use in Anki2 addon 3100585138: Download audio

"""
Download pronunciations from Forvo dictionary using API key
"""

import urllib
import urllib2
import sys
import json
from .forvoRequest import forvoRequest

from .downloader import AudioDownloader, uniqify_list
from ..download_entry import DownloadEntry

apikey = '' # User's forvo API key

class ForvoDownloader(AudioDownloader):
    """Download audio from Forvo"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.base_url = u'http://www.forvo.com'
        self.file_extension = u'.mp3'

        self.APIKEY = apikey

        self.icon_url = 'http://www.forvo.com/'
        self.extras = dict(Source="Forvo")

    def download_files(self, word, base, ruby, split):
        u"""
        Get pronunciations of a word from a Forvo dictionary.
        """
        self.downloads_list = []
        if split:
            # Avoid double downloads
            return
        if not word:
            return
        #lword = word.lower()
        link_list = forvoRequest(word, self.language, self.APIKEY)
        self.maybe_get_icon()
        i = 0
        for lnk in link_list:
            i += 1
            word_path, word_fname = self.get_file_name(word, self.file_extension)
            # sys.stderr.write('fname: %s\n' % word_fname)
            urllib.urlretrieve(lnk, word_fname)
            self.downloads_list.append(DownloadEntry(
                word_path, word_fname, base_name=word, display_text=word,
                file_extension=self.file_extension, extras=self.extras))

