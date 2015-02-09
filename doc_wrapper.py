import sys
import os
import logging

class DocWrapper(object):
    """
    Simple wrapper for effiecnt use of a file
    """
    _doc_name = None
    _doc = []
    
    def __init__(self, filename):
        self._doc_name = filename

    def _load_if_needed(self):
        if len(self._doc) != 0:
            return
        
        f = open(self._doc_name, 'r')
        for line in f:
            self._doc.append(line)

    def len(self):
        self._load_if_needed()
        return len(self._doc)

    def element(self, index):
        self._load_if_needed()
        if index > len(self._doc):
            return None

        return self._doc[index]

    def name(self):
        return self._doc_name

    def digits_needed_for_display(self):
        self._load_if_needed()

        n = 1
        num = self.len()
        while True:
            if abs(num) < 10:
                return n

            num /= 10
            n += 1
