Smart Recovery Meetings
===
Run this like so.

    ./run.sh

Results go to `smart.csv`.

## In detail
Here are directions for running each step at a time.

Download the webpage.

    ./download.sh

Parse it to SQLite.

    ./parse.py

Save as CSV.

    sqlite3 -header -csv /tmp/smart.db 'SELECT * FROM smart;' > smart.csv
