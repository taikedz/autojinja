#!/bin/bash

cd "$(dirname "$0")"

add_pypath() {
	local rcfile="$1"; shift
	local path_to_add="$1"; shift

	if grep -qP PYTHONPATH "$rcfile"; then
		if grep -P '^\s*(export)?\s*PYTHONPATH' "$rcfile" | grep "$path_to_add"; then
			return
		fi
	fi
	echo "export PYTHONPATH=\"\$PYTHONPATH:$path_to_add\"" >> "$rcfile"
}

add_autojinja_lib() {
	local dest_path="$1"; shift

	mkdir -p "$dest_path"
	cp "$maindir" -r "$dest_path/"
}

get_dest_path() {
	local rootpath="/usr/share/lib/pylibs"
	local userpath="$HOME/.local/lib/pylibs"

	if [[ "$UID" = 0 ]]; then
		echo "$rootpath"
	else
		echo "$userpath"
	fi
}

get_dest_bin() {
	if [[ "$UID" = 0 ]]; then
		echo "/usr/bin"
	else
		mkdir -p "$HOME/.local/bin"
		echo "$HOME/.local/bin"
	fi
}

get_dest_rc() {
	if [[ "$UID" = 0 ]]; then
		echo "/etc/bash.bashrc"
	else
		echo "$HOME/.bashrc"
	fi
}

maindir=autojinja

thepath="$(get_dest_path)"
add_autojinja_lib "$thepath"
add_pypath "$(get_dest_rc)" "$thepath"

ln -s "$thepath/$maindir/run-autojinja" "$(get_dest_bin)/autojinja"
