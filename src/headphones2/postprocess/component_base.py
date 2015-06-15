import abc

# a dict of lists of post processors by kind
POST_PROCESSORS = {}


class PostProcessorComponentBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        # registers the post-processor
        if self.group in POST_PROCESSORS:
            POST_PROCESSORS[self.group].append(self)
        else:
            POST_PROCESSORS[self.group] = [self]

    @abc.abstractproperty
    def modifies_file(self):
        raise NotImplementedError

    @abc.abstractproperty
    def group(self):
        raise NotImplementedError

    @staticmethod
    def process(item_list, **kwargs):
        raise NotImplementedError


class PostProcessorException(Exception):
    pass
