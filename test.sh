#!/usr/bin/env sh

test_script() {
    echo "Test script '$1' with '$2'"
    "./$1" "$2" | xmllint --noout - || exit 1
}

test_script "filters/twitter.py" "https://twitter.com/lwnnet"
