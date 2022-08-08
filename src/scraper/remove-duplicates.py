#!/usr/bin/env python

import sys
import pandas as pd

def main():
    '''
    Count releases before and after de-duplication.
    '''
    data = pd.read_csv(sys.argv[1])
    num_packages = len(data)
    data = data.assign(Stripped=data['Release'].str.replace(r'\.(tar\.gz|tar|whl|egg|zip|exe)$', ''))
    result = pd.DataFrame({'Complete': data.groupby('Package').Release.nunique(),
                           'Stripped': data.groupby('Package').Stripped.nunique()})
    num_shorter = len(result[result.Complete > result.Stripped])
    print(f'{num_shorter} / {num_packages} ({(100 * num_shorter / num_packages):6.2}%) shorter')

if __name__ == '__main__':
    main()
