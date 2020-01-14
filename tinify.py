#!/usr/bin/env python
from __future__ import unicode_literals
import bibtexparser
import argparse
import datetime
import codecs


class ConferenceIdentifier(object):
    def __init__(self, booktitle_rules=None, link_rules=None):
        self.booktitle_rules = booktitle_rules
        self.link_rules = link_rules

    def __call__(self, entry):
        if 'booktitle' in entry and self.booktitle_rules is not None:
            booktitle = ' '.join(entry['booktitle'].splitlines())
            booktitle_rules = self.booktitle_rules
            if not isinstance(booktitle_rules, list):
                booktitle_rules = [booktitle_rules]
            for rule in booktitle_rules:
                if rule in booktitle:
                    return True
        if 'link' in entry and self.link_rules is not None:
            link_rules = self.link_rules
            if not isinstance(link_rules, list):
                link_rules = [link_rules]
            for rule in link_rules:
                if rule in entry['link']:
                    return True
        return False


class ConferenceNameShortener(object):
    def __init__(self, shortname, deliminator='-', year_format='%Y'):
        self.shortname = shortname
        self.deliminator = deliminator
        self.year_format = year_format

    def __call__(self, entry):
        assert 'year' in entry
        return self.shortname


class NIPSShortner(object):
    def __call__(self, entry):
        return entry['booktitle'].replace('Advances in Neural Information Processing Systems', 'NIPS')


conferences = [
    (ConferenceIdentifier(['Conference of the North American Chapter of the Association for Computational Linguistics',
                           'Human Language Technology Conference of the NAACL',
                           'NAACL-']), ConferenceNameShortener('NAACL')),
    (ConferenceIdentifier(['European Chapter of the Association for Computational Linguistics',
                           'EACL-']), ConferenceNameShortener('EACL')),
    (ConferenceIdentifier(['Annual Meeting of the Association for Computational Linguistics',
                           'Annual Meeting of the Association of Computational Linguistics',
                           'Annual Meeting of the ACL',
                           'Meeting of the Association for Computational Linguistics',
                           'Annual Meeting on Association for Computational Linguistics',
                           'ACL-']), ConferenceNameShortener('ACL')),
    (ConferenceIdentifier(['Conference on Empirical Methods in Natural Language Processing',
                           'EMNLP-']), ConferenceNameShortener('EMNLP')),
    (ConferenceIdentifier('Conference on Computational Natural Language Learning'),
     ConferenceNameShortener('CoNLL')),
    (ConferenceIdentifier(['International Conference on Computational Linguistics',
                           'Coling-',
                           'COLING-']), ConferenceNameShortener('Coling', deliminator=' ')),
    (ConferenceIdentifier('International Joint Conference on Natural Language Processing'),
     ConferenceNameShortener('IJCNLP')),
    (ConferenceIdentifier('International Conference on Parsing Technologies'),
     ConferenceNameShortener('IWPT', '')),
    (ConferenceIdentifier('International Conference on Machine Learning'),
     ConferenceNameShortener('ICML', ' ', '\'%y')),
    (ConferenceIdentifier(['International Joint Conference on Artifical Intelligence',
                           'International Joint Conference on Artificial Intelligence']),
     ConferenceNameShortener('IJCAI', '', '\'%y')),
    (ConferenceIdentifier('Conference in Uncertainty in Artificial Intelligence'),
     ConferenceNameShortener('UAI', ' ', '\'%y')),
    (ConferenceIdentifier('International Conference on Language Resources and Evaluation'),
     ConferenceNameShortener('LREC')),
    (ConferenceIdentifier('International Conference on Artificial Intelligence and Statistics'),
     ConferenceNameShortener('AISTATS')),
    (ConferenceIdentifier('ACM SIGKDD International Conference on Knowledge Discovery and Data Mining'),
     ConferenceNameShortener('KDD')),
    (ConferenceIdentifier('Advances in Neural Information Processing Systems'), NIPSShortner()),
]


def get_shorten_booktitle(entry, conference_name_pattern='Proc. of {0}'):
    for identifier, shortener in conferences:
        if identifier(entry) and 'year' in entry:
            return conference_name_pattern.format(shortener(entry))
    return entry['booktitle'].replace('Proceedings', 'Proc.')


def main():
    cmd = argparse.ArgumentParser()
    cmd.add_argument('-input', help='the path to the filename.')
    cmd.add_argument('-output', help='the path to the filename.')
    opt = cmd.parse_args()

    with codecs.open(opt.input, 'r', encoding='utf-8') as fpi, codecs.open(opt.output, 'w', encoding='utf-8') as fpo:
        db = bibtexparser.load(fpi)
        for entry in db.entries:
            if entry['ENTRYTYPE'].lower() == 'inproceedings':
                if 'pages' in entry:
                    del entry['pages']
                if 'address' in entry:
                    del entry['address']
                if 'month' in entry:
                    del entry['month']
                if 'editor' in entry:
                    del entry['editor']
                if 'series' in entry:
                    del entry['series']
                if 'publisher' in entry:
                    del entry['publisher']
                if 'booktitle' in entry:
                    entry['booktitle'] = get_shorten_booktitle(entry)
            elif entry['ENTRYTYPE'].lower() == 'incollection':
                if 'publisher' in entry:
                    del entry['publisher']
                if 'editor' in entry:
                    del entry['editor']
                if 'booktitle' in entry:
                    entry['booktitle'] = get_shorten_booktitle(entry, '{0}')

        bibtexparser.dump(db, fpo)


if __name__ == "__main__":
    main()
