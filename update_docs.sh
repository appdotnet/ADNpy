#! /usr/bin/env bash

cd docs;
make html;
rsync -avzt _build/html ~/Dropbox/Public/Stash/adnpy_dev_docs;