from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import yaml


def clean_cassette_from_bad_requests(cassette_path, output_path):
    """
    Removing all failed interactions left over from recording greatly improves test suite running time.
    :param cassette_path:
    :param output_path:
    :return:
    """
    with open(cassette_path) as input_cassette, open(output_path, 'wb') as output:
        in_c = yaml.load(input_cassette)

        good_interactions = [interaction for interaction in in_c['interactions'] if
                             interaction['response']['status']['code'] != 503]
        new = dict(version=in_c['version'], interactions=good_interactions)

        yaml.dump(new, output)
