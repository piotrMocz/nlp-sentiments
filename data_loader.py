from os import listdir, getcwd
from os.path import isfile, join, splitext
import file_utils


def load_filenames(dir_path):
    """
    Scans through the files in the directory to extract the info from filenames
    :param dir_path: directory to scan
    :return: list of dicts containing info about the files
    """
    def strip_ext(filename):
        return splitext(filename)[0]

    def parse_tags(filename):
        bill_id, spkr_id, _, PMV = strip_ext(filename).split('_')
        party, mention_type, vote = PMV
        vote_bool = (vote == 'Y')
        return {'bill_id': int(bill_id),
                'spkr_id': int(spkr_id),
                'party': party,
                'mention_type': mention_type,
                'vote': vote_bool,
                'filename': filename}

    filenames = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    file_tags = [parse_tags(fname) for fname in filenames]

    return file_tags


def filter_feats(infos, feat_type):
    """
    Returns only the entries with a "Y" or "N" vote
    :param infos: List of dictionaries returned by `load_filenames`.
    :param feat_type: Vote type: "Y" or "N"
    :return: Filtered list of entries.
    """
    filter_fun = lambda info: info['vote'] if feat_type == 'pos' else not info['vote']
    return filter(filter_fun, infos)
