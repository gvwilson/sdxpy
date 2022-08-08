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


index_response = requests.get(f'{DOMAIN}/simple/')
print('Package,Releases')
all_packages = RE_PACKAGE.findall(index_response.text)
for package in all_packages:
    name = package.strip('/').split('/')[-1]
    url = f'{DOMAIN}{package}'
    package_response = requests.get(url)
    count = len(RE_RELEASE.findall(package_response.text))
    print(f'{name},{count}')
