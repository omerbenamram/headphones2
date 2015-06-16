import abc


class PostProcessorComponentBase(object):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def process(item_list, **kwargs):
        raise NotImplementedError


class PostProcessorException(Exception):
    pass
