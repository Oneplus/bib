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
        date = datetime.datetime.strptime(entry['year'], '%Y')
        year = datetime.datetime.strftime(date, self.year_format)
        return '{0}{1}{2}'.format(self.shortname, self.deliminator, year)


conferences = {
    'ACL': (ConferenceIdentifier(['Annual Meeting of the Association for Computational Linguistics',
                                  'Annual Meeting of the Association of Computational Linguistics',
                                  'Annual Meeting of the ACL',
                                  'Meeting of the Association for Computational Linguistics',
                                  'Annual Meeting on Association for Computational Linguistics']),
            ConferenceNameShortener('ACL')),
    'EMNLP': (ConferenceIdentifier('Conference on Empirical Methods in Natural Language Processing'),
              ConferenceNameShortener('EMNLP')),
    'NAACL': (ConferenceIdentifier(['Conference of the North American Chapter of the Association for '
                                    'Computational Linguistics',
                                    'Human Language Technology Conference of the NAACL']),
              ConferenceNameShortener('NAACL')),
    'CoNLL': (ConferenceIdentifier('Conference on Computational Natural Language Learning'),
              ConferenceNameShortener('CoNLL')),
    'Coling': (ConferenceIdentifier('International Conference on Computational Linguistics'),
               ConferenceNameShortener('Coling', deliminator=' ')),
    'IJCNLP': (ConferenceIdentifier('International Joint Conference on Natural Language Processing'),
               ConferenceNameShortener('IJCNLP')),
    'IWPT': (ConferenceIdentifier('International Conference on Parsing Technologies'),
             ConferenceNameShortener('IWPT', '')),
    'ICML': (ConferenceIdentifier('International Conference on Machine Learning'),
             ConferenceNameShortener('ICML', ' ', '\'%y')),
    'IJCAI': (ConferenceIdentifier(['International Joint Conference on Artifical Intelligence',
                                    'International Joint Conference on Artificial Intelligence']),
              ConferenceNameShortener('IJCAI', '', '\'%y')),
    'EACL': (ConferenceIdentifier('European Chapter of the Association for Computational Linguistics'),
             ConferenceNameShortener('EACL')),
    'UAI': (ConferenceIdentifier('Conference in Uncertainty in Artificial Intelligence'),
            ConferenceNameShortener('UAI', ' ', '\'%y')),
    'LREC': (ConferenceIdentifier('International Conference on Language Resources and Evaluation'),
             ConferenceNameShortener('LREC'))
}


def get_shorten_booktitle(entry):
    conference_name_pattern = 'Proc. of {0}'
    for name, (identifier, shortener) in conferences.items():
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
            if entry['ENTRYTYPE'].lower() != 'inproceedings':
                continue
            if 'pages' in entry:
                del entry['pages']
            if 'address' in entry:
                del entry['address']
            if 'month' in entry:
                del entry['month']
            if 'booktitle' in entry:
                entry['booktitle'] = get_shorten_booktitle(entry)
            if 'publisher' in entry:
                publisher = entry['publisher']
                publisher = publisher.replace('Association for Computational Linguistics', 'ACL')
                publisher = publisher.replace('European Language Resources Association (ELRA)', 'ELRA')
                entry['publisher'] = publisher

        bibtexparser.dump(db, fpo)


if __name__ == "__main__":
    main()
