#!/usr/bin/python

from autojinja import render_template
import sys

def do_render(templatef, args):
    try:
        res = render_template(templatef, args)
        print(res)
    except ValueError as e:
        sys.stderr.write("\n%s\n" % e)


def main():
    if len(sys.argv) < 2:
        print("Supply a template file to process")
        sys.exit(1)

    template_file = sys.argv[1]

    # Remove the first argument (script name) so that the name that shows up in help is the template's
    sys.argv = sys.argv[1:]

    if len(sys.argv) < 3:
        do_render(template_file, [])
        exit()

    do_render(template_file, sys.argv[1:]) # From 1, because we walloped an argument

if __name__ == "__main__":
    main()
