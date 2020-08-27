#!/usr/bin/env python3

import os
import sys
import json

import progressbar

from lunr import lunr

from py_dataset import dataset

from eprintviews import Subjects

#
# Apply scheme setups the data for search results and indexing.
#
def apply_scheme(obj, subjects, htdocs):
    o = {}
    subject_keys = subjects.get_keys()
    # NOTE: simple fields
    for field in [ '_Key', 'title', 'date', 'year', 'type', 'collection', 'interviewer', 'interviewdate', 'depositor', 'deposit_date', 'issn', 'doi' ]:
        if (field in obj) and (obj[field] != None) and (obj[field] != ''):
            o[field] = obj[field]
        else:
            o[field] = ''
    if len(o) == 0:
        return {}, 'No fields found'
    # NOTE: the following fields require special handling as they maybe arrays.

    if 'creators' in obj:
        creators = []
        for creator in obj['creators']:
            display_name = ''
            if 'display_name' in creator:
                display_name = creator['display_name']
            if display_name != '':
                if not display_name in 'creators':
                    creators.append(display_name)
        if len(creators) > 0:
            o['creators'] = '; '.join(creators)
    if ('subjects' in obj) and (len(obj['subjects']) > 0):
        terms = []
        for term in obj['subjects']['items']:
            if term in subject_keys:
                terms.append(subjects.get_subject(term))
        o['subjects'] = '; '.join(terms)
    else:
        o['subjects'] = ''
    if ('keywords' in obj) and (len(obj['keywords']) > 0):
        terms = []
        if isinstance(obj['keywords'], str):
            if term in subject_keys:
                terms.append(subjects.get_subject(term))
            else:
                terms.append(term)
        o['keywords'] = ' '.join(terms)                
    else:
        o['keywords'] = ''
    if ('abstract' in obj) and (len(obj['abstract']) > 0):
        o['abstract'] = obj['abstract'].strip()
    else:
        o['abstract'] = ''
    # Now we can dumps our scheme and hande back the object of indexing
    if len(o) > 0:
        src = json.dumps(o)
        key = o['_Key']
        scheme_json = os.path.join(htdocs, f'{key}', 'scheme.json')
        with open(scheme_json, 'w') as f:
            f.write(src);
        return o, ''
    else:
        return {}, 'No fields found'

def get_fields(obj):
    fields = []
    for f in obj:
        fields.append(f)
    return fields

def build_index(c_name, htdocs, f_subjects):
    subjects = Subjects()
    subjects.load_subjects(f_subjects)
    keys = dataset.keys(c_name)
    tot = len(keys)
    documents = []
    e_cnt = 0
    bar = progressbar.ProgressBar(
            max_value = tot,
            widgets = [
                progressbar.Percentage(), ' ',
                progressbar.Counter(), f'/{tot} ',
                progressbar.AdaptiveETA(),
                f' indexed from {c_name}'
            ], redirect_stdout=False)
    for i, key in enumerate(keys):
        obj, err = dataset.read(c_name, key)
        if err != '':
            print(f'WARNING: skipping {key} in {c_name}, {err}')
            e_cnt += 1
            continue
        obj, err = apply_scheme(obj, subjects, htdocs)
        if err != '':
            print(f'WARNING: skipping {kay} in {c_name}, apply scheme: {err}')
            e_cnt += 1
            continue
        documents.append(obj)
        bar.update(i)
    bar.finish()
    print(f'Found {len(documents)} in {c_name}')
    idx = lunr(
        ref = '_Key',
        fields=get_fields(obj),
        documents = documents
    )
    print(f'indexed {len(documents)} documents')
    i_name = os.path.join(htdocs, 'documents.json')
    with open(i_name, 'w') as f:
        src = json.dumps(idx.serialize())
        f.write(src)
    print(f'wrote {i_name} based on {c_name}')

if __name__ == "__main__":
    f_name = ''
    htdocs = 'htdocs'
    c_name = ''
    f_subjects = ''
    if len(sys.argv) > 1:
        f_name = sys.argv[1]
    if f_name == '':
        print(f'Missing configuration filename.')
        sys.exit(1)
    if not os.path.exists(f_name):
        print(f'Missing {f_name} configuration file.')
        sys.exit(1)

    with open(f_name) as f:
        src = f.read()
        cfg = json.loads(src)
        if 'htdocs' in cfg:
            htdocs = cfg['htdocs']
        if 'dataset' in cfg:
            c_name = cfg['dataset']
        if 'subjects' in cfg:
            f_subjects = cfg['subjects']

    if c_name == '':
        print(f'''Missing collection name in {f_name}.''')
        sys.exit(1)
    if not os.path.exists(c_name):
        print(f'''Cannot find "{c_name}" collection from {f_name}.''')
        sys.exit(1)
    if not os.path.exists(htdocs):
        print(f'''Cannot find the htdocs directory''')
        sys.exit(1)
    build_index(c_name, htdocs, f_subjects)
