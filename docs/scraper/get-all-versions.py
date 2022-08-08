#!/usr/bin/env python

import sys
import argparse
import requests
import re
import csv
import time


# Match package URL in main index page.
RE_PACKAGE = re.compile(r'<a href="(.+?)">')

# Match release URL in package index page.
RE_RELEASE = re.compile(r'<a href=".+?">(.+?)</a>')

# PyPI base URL
BASE_URL = 'https://pypi.org/simple/'


def main():
    '''
    Main driver.
    '''
    args = parse_args()
    all_packages = get_package_list(args)
    progress = initialize_progress(args, all_packages)
    writer = csv.writer(sys.stdout, lineterminator='\n')
    writer.writerow(['Package', 'Release'])
    for package in all_packages:
        get_package_info(package, writer)
        report_progress(progress)


def parse_args():
    '''
    Parse command-line arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--restart', type=str, help='restart from this package')
    parser.add_argument('--verbose', action='store_true', help='show progress')
    return parser.parse_args()


def get_package_list(args):
    '''
    Get main package listing page and extract values.
    '''
    response = requests.get(f'{BASE_URL}')
    assert response.status_code == 200, \
        f'Unexpected status for index page {response.status_code}'
    all_packages = RE_PACKAGE.findall(response.text)
    all_packages = [p.strip('/').split('/')[-1] for p in all_packages]
    if (args.restart):
        start = all_packages.index(args.restart)
        if (start < 0):
            print(f'Unable to find {args.restart} in package list',
                  file=sys.stderr)
            sys.exit(1)
        all_packages = all_packages[start:]
    return all_packages


def get_package_info(name, writer):
    '''
    Get and print information about a specific package.
    '''
    url = f'{BASE_URL}{name}'
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Unexpected status for package page {url}: {response.status_code}',
              file=sys.stderr)
        writer.writerow([name, 'NA'])
    else:
        all_releases = RE_RELEASE.findall(response.text)
        for release in all_releases:
            writer.writerow([name, release])


def initialize_progress(args, packages):
    '''
    Initialize record keeping for progress monitoring.
    '''
    return {
        'report': args.verbose,
        'start': time.time(),
        'expected': len(packages),
        'seen': 0
    }


def report_progress(progress):
    '''
    Report progress, updating the progress record as a side effect.
    '''
    if (not progress['report']):
        return
    progress['seen'] += 1
    if (progress['seen'] % 10) == 0:
        elapsed = time.time() - progress['start']
        duration = progress['expected'] * elapsed / progress['seen']
        print(f"{progress['seen']} @ {elapsed:.1f} / {progress['expected']} @ {duration:.1f}",
              file=sys.stderr)


if __name__ == '__main__':
    main()
