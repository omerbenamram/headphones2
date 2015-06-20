import abc


class PostProcessor(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    def process(self, item_list, **kwargs):
        """
        Performs all function logic, files should not be modified when calling process
        :param item_list:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def write(self, item_list, **kwargs):
        """
        Performs all I/O related calls
        :return:
        """
        raise NotImplementedError()


class PostProcessorException(Exception):
    pass
