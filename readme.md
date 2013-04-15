Smart Recovery Meetings
===
Download the webpage.

    ./download.sh

Parse it to SQLite.

    ./parse.py

Save as CSV.

    sqlite3 -header -csv /tmp/smart.db 'SELECT * FROM smart;' > smart.csv
