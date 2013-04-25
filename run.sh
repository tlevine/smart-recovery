#!/bin/sh
set -e

# Download
test -f showall.php || ./download.sh

# Clear database
rm -f /tmp/smart.db
./parse.py

# Build csv
sqlite3 -header -csv /tmp/smart.db 'SELECT * FROM smart;' > smart.csv

# Check results
./qa.r
