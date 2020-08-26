#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from os import walk
from debian.deb822 import Packages
from time import gmtime, strftime
from jinja2 import Template

DISTS_DIR = "dists"

TEMPLATE = \
"""
<table class="table table-condensed table-hover">
<th>Name</th><th>Version</th><th>Description</th><th>Suite</th>
{% for package in packages_data %}
<tr>
	<td>
		<span title="{{ package.desc }}">
			<a href="{{ package.filename }}">{{ package.name }}</a>
		</span>
	</td>
	<td>{{ package.version }}</td>
	<td>{{ package.desc }}</td>
	<td><a href="https://www.debian.org/releases/{{ package.suite }}/">{{ package.suite }}<a></td>
</tr>
{% endfor %}
</table>

Last update: {{last_update}} by <a href="{{script}}">{{script}}</a>
"""

OUTPUT_FILE = 'packages.html'

packages_data = []

# want the generator as list reversed (because want sid at last)
for files in reversed(list(walk(DISTS_DIR))):
    for f in files:
        for packages in f:
            if packages == "Packages":
                packages_file = "{}/{}".format(files[0], packages)
                for package in Packages.iter_paragraphs(open(packages_file)):
                    if "dbg" not in package['Package']:
                        packages_data.append({'name': package['Package'],
                                              'suite': files[0].split('/')[1],
                                              'version': package['Version'],
                                              'filename': "/".join(package['Filename'].split("/")[:-1]),
                                              'desc': package['Description'].split("\n")[0]})

t = Template(TEMPLATE)
with open(OUTPUT_FILE, 'w') as output:
    datas = {'packages_data': packages_data,
             'last_update': strftime("%a, %d %b %Y %H:%M:%S +0100", gmtime()),
             'script': __file__
            }
    output.write(t.render(datas))
