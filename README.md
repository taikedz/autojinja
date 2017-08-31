# Auto-Jinja

A tool to process jinja2 templates that define their own arguments. 

Typical use case would be processing collections of configs that each require different treatment; rather than have the requirement logic in the program, move it to the template and pass the user arguments along.

## Install as a command

Rerquires a Linux/UNIX environment.

	git clone https://github.com/taikedz/autojinja
	autojinja/install.sh

Run the install step as root to make autojinja available to all.

Run it on a parameterised template - for example

	autojinja examples/nagios-host.template -n example -a example.com -d "Example.com server"

which will print the expanded template to stdout.

## Install as a library

Linux, Mac and Windows.

Clone the autojinja repository to a location on your `PYTHONPATH`.

### Template example

Given this nagios template file in `./nagios-host.template`:

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
	
	autojinja examples/nagios-host.cfg -n host -a addr

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

The template header is a series of lines starting either with `#:o` or `#:r`; these are the specification lines. There must be no lines above the header.

Header lines are composed of 4 fields:

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

The `render_template` function performs a jinja2 rendering; if there was an error, a ValueError is raised, containing a help message specifying the expected arguments pattern, as well as the first missing argument identified.

	import autojinja
	
	try:
		rendered_template = autojinja.render_template("path/to/template",
							     ["-l", list of arguments",
							     "-w", "with their argument identifiers"])
	except ValueError as e:
		print(e)
