#!/usr/bin/env python

import sys
import pandas as pd
from collections import Counter

def main():
    '''
    Count frequency of '.'-separated components of names.
    '''
    data = pd.read_csv(sys.argv[1])
    data = data['Release'].str.split('.', expand=True)
    data = data.values.flatten()
    data = Counter(data)
    del data[None]
    data = pd.DataFrame.from_dict(data, orient='index').reset_index()
    data = data.rename(columns={'index': 'Component', 0: 'Count'})
    data = data[~ data['Component'].str.match(r'^\d+$', na=False)]
    data = data.sort_values(by='Count', ascending=False)
    data.to_csv(sys.stdout, header=True, index=False)


if __name__ == '__main__':
    main()
