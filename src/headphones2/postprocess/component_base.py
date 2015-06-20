import abc


class PostProcessorComponentBase(object):
    __metaclass__ = abc.ABCMeta

    def process(item_list, **kwargs):
        raise NotImplementedError()


class PostProcessorException(Exception):
    pass
