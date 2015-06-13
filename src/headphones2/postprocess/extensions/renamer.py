import shutil
from headphones2.postprocess.component_base import PostProcessorComponentBase


class Renamer(PostProcessorComponentBase):

    kind = 'extension'

    def __init__(self):
        super(PostProcessorComponentBase, self).__init__()

    @staticmethod
    def process(item_list, name_string=None, destination_folder=None, release_id=None):
        pass
