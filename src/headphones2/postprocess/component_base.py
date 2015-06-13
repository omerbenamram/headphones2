import abc

# a dict of lists of post processors by kind
POST_PROCESSORS = {}


class PostProcessorComponentBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        # registers the post-processor
        POST_PROCESSORS[self.kind].append(self)

    @abc.abstractproperty
    def kind(self):
        raise NotImplementedError

    @staticmethod
    def process(item_list, **kwargs):
        raise NotImplementedError


class PostProcessorException(Exception):
    pass
