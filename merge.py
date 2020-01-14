#!/usr/bin/env python
from __future__ import unicode_literals
import bibtexparser
import argparse
import codecs


def merge(dbs):
    default_writer = bibtexparser.bwriter.BibTexWriter()

    outputs = {}
    for db in dbs:
        for entry in db.entries:
            key = entry['ID']
            output = default_writer._entry_to_bibtex(entry)
            if key in outputs:
                continue
            outputs[key] = output
    return bibtexparser.loads('\n\n'.join([v for k, v in outputs.items()]))


def main():
    cmd = argparse.ArgumentParser()
    cmd.add_argument('-inputs', nargs='+', help='the path to the filename.')
    cmd.add_argument('-output', help='the path to the filename.')
    opt = cmd.parse_args()

    dbs = []
    for inp in opt.inputs:
        with codecs.open(inp, 'r', encoding='utf-8') as fpi:
            dbs.append(bibtexparser.load(fpi))

    with codecs.open(opt.output, 'w', encoding='utf-8') as fpo:
        bibtexparser.dump(merge(dbs), fpo)


if __name__ == "__main__":
    main()
