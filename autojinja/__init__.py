#!/usr/bin/python

from jinja2 import Template
import sys
import re
import argparse

def is_blank(line):
    return None != re.match("^(\\s*)$", line)

def arg_tokens_of(line):
    return re.match("^#:(r|o)\\s+(-[a-zA-Z0-9-]+)\\s+([a-zA-Z0-9]+)\\s+(.+)$", line)

def is_required(character):
    if character == "r":
        return True
    elif character == "o":
        return False

    raise ValueError("Error in template definition: %s is not a valid requirement state"%character)

def get_template_args(path, supplied_args):
    fh = open(path)
    lines = fh.readlines()
    fh.close()

    return args_from_lines(lines, supplied_args)

def args_from_lines(lines, supplied_args):
    argsp = argparse.ArgumentParser()
    i = 0
    for line in lines:
        tokens = arg_tokens_of(line)

        if not tokens and not is_blank(line):
            break

        i = i+1
        if is_blank(line):
            continue

        required    = is_required(tokens.group(1))
        marker      = tokens.group(2)
        varname     = tokens.group(3)
        description = tokens.group(4).strip()

        argsp.add_argument(marker, "--"+varname, help=description, required=required)

    return argsp.parse_args(supplied_args).__dict__ , lines[i:]

class StringCollector:

    def __init__(self):
        self.strings = []

    def write(self, newstring):
        self.strings.append(newstring)

    def writelines(self, stringlist):
        self.strings.extend(stringlist)

    def __str__(self):
        return "".join(self.strings )

    def close(self):
        return True

def render_template(path, supplied_args):
    # We want to catch the stderr output
    # we shim a fake stderr temporarily
    oldstderr = sys.stderr
    collector = StringCollector()
    sys.stderr = collector
    output = ""
    err = None

    try:
        args,lines = get_template_args(path, supplied_args)
        template = Template("".join(lines))

        output = template.render(args)
    except SystemExit as e:
        # Unlike the general case, this section may produce an error
        # (bad data passed to the collector possible?), so we
        # reinstate the real stderr asap
        sys.stderr = oldstderr

        err = ValueError( collector )
    except Exception as e:
        err = e

    sys.stderr = oldstderr

    if err:
        raise err

    return output
