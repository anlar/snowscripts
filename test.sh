#!/usr/bin/env sh

test_filter() {
    echo "Test filter '$1' with '$2'"
    wget -q -O - "$2" | "$1" | xmllint --noout - || exit 1
}

test_filter "filters/twitter.py" "https://twitter.com/lwnnet"
