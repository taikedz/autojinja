#!/usr/bin/python

from jinja2 import Template
import sys
import re
import argparse

def get_template_args(path, supplied_args):
    fh = open(path)
    lines = fh.readlines()
    fh.close()

    return args_from_lines(lines, supplied_args)

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

def args_from_lines(lines, supplied_args):
    argsp = argparse.ArgumentParser()
    i = 0
    for line in lines:
        i = i+1
        tokens = arg_tokens_of(line)
        if not tokens:
            if is_blank(line):
                continue
            break

        required    = is_required(tokens.group(1))
        marker      = tokens.group(2)
        varname     = tokens.group(3)
        description = tokens.group(4).strip()

        argsp.add_argument(marker, "--"+varname, help=description, required=required)

    return argsp.parse_args(supplied_args).__dict__,lines[i:]

def combine(path, supplied_args):
    oldstderr = sys.stderr
    nullhandler = open("/dev/null", "w") # FIXME this needs to be something we can read from, to get back the error emssage
    sys.stderr = nullhandler
    output = ""
    err = None

    try:
        args,lines = get_template_args(path, supplied_args)
        template = Template("".join(lines))

        output = template.render(**args)
    except SystemExit as e:
        err = ValueError("Renderer returned err %i with no message."%e)
    except Exception as e:
        err = e

    nullhandler.close()
    sys.stderr = oldstderr

    if err:
        raise err

    return output

def process_template(path, supplied_args):
    args,lines = get_template_args(path, supplied_args)
    template = Template( "".join(lines) )

    return template.render(**args)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Supply a template file to process")
        sys.exit(1)

    template_file = sys.argv[1]

    # Remove the executable and the template from the command list so it does not appear in the help
    sys.argv = [""] + sys.argv[2:]

    print( process_template(template_file, sys.argv[1:]) ) # From 1, because we walloped an argument
