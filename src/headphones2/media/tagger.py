from abc import ABCMeta


class Tagger(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @staticmethod
    def process(item_list):
        raise NotImplementedError
