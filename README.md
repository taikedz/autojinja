# Auto-Jinja

A tool to process jinja2 templates that define their own arguments. 

## Install

Rerquires a Linux/UNIX environment.

Add the `autojinja/` directory to your `PYTHONPATH`, and the `bin/` directory to your `PATH` (or, copy these to directories in the respective paths)

## Example

Example direct usage:

	PYTHONPATH=./ bin/autojinja examples/technician.txt

The above will print the arguments that the template `technician.txt` requires for being populated, to stderr.

	PYTHONPATH=./ bin/autojinja examples/technician.txt -n Guido -l "python, c"

The above will render the template to stdout.

### Template example

Given this nagios template file in `./nagios-service.template`:

	#:r -n name              The shortname for the host, to use in nagios
	#:r -a address           The IP or FQDN of the host

	#:o -t template          Generic template to use (default "generic-host")
	#:o -r register          Whether to register the host, set to 0 if host template (default "1")
	#:o -d description       The description for the host (optional)
	#:o -c contacts          The contacts for the host (optional)
	#:o -g contactgroups     The contact groups of the host (optional)
	#:o -u notesurl          The url where the operator can find more information on the host (optional)

	define host{
		use                             {{template | default("generic-host", true)}}
		register                        {{register | default("1", true)}}
		host_name			{{name}}
		alias				{{description | default("Host %s"%name)}}
		address				{{address}}
		check_command			check-host-alive
	{% if contacts %}
		contacts                        {{contacts}} {% endif %}
	{% if contactgroups %}
		contact_groups			{{contactgroups}} {% endif %}
	{% if notesurl %}
		notes_url			{{notesurl}} {% endif %}
	}

we can run
	
	PYTHONPATH=. bin/autojinja examples/nagios-host.cfg -n host -a addr

which will output:

	define host{
		use                             generic-host
		register                        1
		host_name                       host
		alias                           None
		address                         addr
		check_command                   check-host-alive



	}

*(Note - the extra whitespace is due to the space outwith the conditional sections in the template)*

Simply running without arguments will complain about missing mandatory arguments, and print the required arguments list..

## Template Header Syntax

The template must specify at the top of the file the arguments it expects, as 4 fields:

* `#:r` or `#:o` - defining whether the the argument is required, or optional
* an argument identifier, e.g. `-n`
* a shortname, corresponding to the variable used in the template, e.g. `myvariable`
* a description

Once a non-header, non-empty line is found, the template proper begins; the header is not printed in the output.

Due to the use of the `argparse` library to support dynamically creating arguments, some restrictions apply:

* the argument identifier must be a single dash and a single letter
* the argument identifier must not be `-h` as this is a reserved item
* the shortname may only contain alphanumeric characters: a-z, A-Z, 0-9. No dots, dashes or underscores are allowed.

## As a library

You can use autojinja as a python library:

	import autojinja
	autojinja.render_template("path/to/template", ["-l", list of argumentsf", "-w", "with their argument identifiers"])

With `render_template`, if the arguments supplied do not meet all requirements, the help will be printed to stderr, and the program will exit.

With `combine`, the rendered text is simply returned; if there was an error, a ValueError is raised, and the error message is silenced.

	import autojinja
	rendered_template = autojinja.combine("path/to/template", ["-l", list of arguments", "-w", "with their argument identifiers"])
