# Auto-Jinja

A tool to process jinja2 templates that define their own arguments.

For example, given this template file in `./myfile.template`:

	#:r -n name A person's name
	#:o -t tenure The person's length of service
	#:o -p period Period counted

	My name is {{name}}.
	{% if tenure %}
	I have worked here for {{tenure}} {{period|default("years",true)}}.
	{% endif %}

we can run
	
	python lib/autojinja.py ./myfile.template -n Tux -t 26

which will output:

	My name is Tux.

	I have worked here for 26 years.

Simply running without arguments will complain about missing mandatory arguments.

## Template Header Syntax

The template must specify at the top of the file the arguments it expects, as 4 fields:

* `#:r` or `#:o` - defining whether the the argument is required, or optional
* an argument identifier
* a shortname, corresponding to the variable used in the template
* a description

Once a non-header, non-empty line is found, the template proper begins and the header is not printed in the output.

## As a library

You can use autojinja as a python library:

	import autojinja
	autojinja.process_template("path/to/template", ["list", "of", "arguments"])

If the arguments supplied do not meet all requirements, the help will be printed, and the program will exit - a side effect of using the `argsparse` library.

You can prevent exiting by catching the `SystemExit` exception. To prevent the error from being output to console, override `stderr`.

	import autojinja
	import sys
	
	oldstderr = sys.stderr
	sys.stderr = None
	try:
		autojinja.process_template("path/to/template", ["list", "of", "arguments"])
	except SystemExit:
		# deal with it
	
	sys.stderr = oldstderr
