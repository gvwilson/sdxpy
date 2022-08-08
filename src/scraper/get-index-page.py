import sys
import requests
import re
import time


# Match package URL in main index page.
RE_PACKAGE = re.compile(r'<a href="(.+?)">')

# Match release URL in package index page.
RE_RELEASE = re.compile(r'<a href=".+?">(.+?)</a>')

# PyPI domain.
DOMAIN = 'https://pypi.org'


# Get main index page.
index_response = requests.get(f'{DOMAIN}/simple/')
assert index_response.status_code == 200, \
    f'Unexpected status for index page {index_response.status_code}'

# Get sub-pages and count releases in each.
num_seen = 0
t_start = time.time()
print('Package,Releases')
all_packages = RE_PACKAGE.findall(index_response.text)
for package in all_packages:
    name = package.strip('/').split('/')[-1]
    url = f'{DOMAIN}{package}'
    package_response = requests.get(url)
    if package_response.status_code != 200:
        print(f'Unexpected status for package page {url}: {package_response.status_code}',
              file=sys.stderr)
        count = 'NA'
    else:
        count = len(RE_RELEASE.findall(package_response.text))
    print(f'{name},{count}')
    num_seen += 1
    if (num_seen % 10) == 0:
        t_elapsed = time.time() - t_start
        t_expected = len(all_packages) * t_elapsed / num_seen
        print(f'{num_seen} @ {t_elapsed:.1f} / {len(all_packages)} @ {t_expected:.1f}',
              file=sys.stderr)
