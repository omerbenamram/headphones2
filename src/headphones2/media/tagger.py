from abc import ABCMeta


class Tagger(object):

    __metaclass__ = ABCMeta

    def __init__(self, task):
        self._task = task

    @property
    def results(self):
        raise NotImplementedError

    def tag(self):
        raise NotImplementedError
