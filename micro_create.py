#!/usr/bin/env python
import sys
import os
import re
import uuid
from jinja2 import Template

TEMPLATE_DIR = "templates"


def main(project_name):
    if os.path.exists(project_name):
        print "Project directory already exists, giving up"
        sys.exit(2)
    os.mkdir(project_name)
    template_dir = TEMPLATE_DIR
    variables = {
        "project_name": project_name,
        "project_secret": str(uuid.uuid4())
    }
    for dirname, _, files in os.walk(template_dir):
        bdir = re.sub("^" + template_dir + "/?", '', dirname)
        ddir = os.path.join(project_name, bdir)
        if not os.path.isdir(ddir):
            os.mkdir(ddir)
        for f in files:
            with open(os.path.join(dirname, f)) as inf:
                tmpl = Template(inf.read())
            dest = os.path.join(ddir, f)
            with open(dest, "w") as outf:
                outf.write(tmpl.render(**variables))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: micro_create.py <project_name>"
        sys.exit(1)
    main(sys.argv[1])