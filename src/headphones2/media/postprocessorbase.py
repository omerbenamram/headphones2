import abc

# holds a list of post processors and their kind
POST_PROCESSORS = {}


class PostProcessorBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        # registers the post-processor
        POST_PROCESSORS[self.kind].append(self)

    @abc.abstractproperty
    def kind(self):
        raise NotImplementedError

    @staticmethod
    def process(item_list):
        raise NotImplementedError


class PostProcessorException(Exception):
    pass
