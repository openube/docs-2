import pytest

from contextlib import redirect_stdout
import re
import ast
import urllib.request
from urllib.error import HTTPError, URLError
from conftest import file_io, LOCALHOST


@file_io
def test_alias(md_filepaths):
    aliases = []
    valid_alias = True
    for line in md_filepaths:
        match = re.match(r'^aliases: \[.*\]', line)
        if match:
            new_line = match.group()
            # Literal evaluation of brackets in alias
            aliases += ast.literal_eval(new_line[new_line.find("["):])
    if md_filepaths.name.lstrip('./content/')[:-3] in \
            [a.rstrip('/') for a in aliases]:
        valid_alias = False
        print('Circular alias: ' + path)
    for alias in aliases:
        try:
            urllib.request.urlopen(LOCALHOST + alias).getcode()
        except HTTPError:
            valid_alias = False
            print('404 alias: ' + alias)
    assert valid_alias == True,'Not a valid alias'

