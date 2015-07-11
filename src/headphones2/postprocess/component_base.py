import abc


class PostProcessor(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    def process(self, item_list, **kwargs):
        """
        Performs all function logic, files should not be modified when calling process, only metadata should be
        appended to item objects
        :param item_list:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

class PostProcessorException(Exception):
    pass
