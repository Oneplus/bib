#!/bin/bash
python merge.py -inputs db.bib $1 -output new_db.bib
mv new_db.bib db.bib

python shorten.py -input $1 -output $1.short
python merge.py -inputs shortdb.bib $1.short -output new_shortdb.bib
mv new_shortdb.bib shortdb.bib

python tinify.py -input $1 -output $1.tiny
python merge.py -inputs tinydb.bib $1.tiny -output new_tinydb.bib
mv new_tinydb.bib tinydb.bib

git add db.bib
git add shortdb.bib
git add tinydb.bib
git commit -m "add $1"

rm $1.short
rm $1.tiny
