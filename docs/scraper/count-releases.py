#!/usr/bin/env python

'''
Count how many releases there are per package.
'''

import sys
import pandas as pd

def main():
    '''
    Main driver.
    '''
    data = pd.read_csv(sys.argv[1])
    result = data.groupby('Package').Release.nunique()
    result.to_csv(sys.stdout, header=True)


if __name__ == '__main__':
    main()
