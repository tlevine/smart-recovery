#!/usr/bin/env Rscript

library(sqldf)
nmeetings <- sqldf('SELECT count(*) FROM smart', dbname = '/tmp/smart.db')[1,1]
has.day <- sqldf('SELECT count(*) FROM smart WHERE Day NOT NULL', dbname = '/tmp/smart.db')[1,1]
has.begin <- sqldf('SELECT count(*) FROM smart WHERE Begin_Time NOT NULL', dbname = '/tmp/smart.db')[1,1]
has.end <- sqldf('SELECT count(*) FROM smart WHERE End_Time NOT NULL', dbname = '/tmp/smart.db')[1,1]

cat(sprintf('Of %d meetings, I managed to parse the day of the week from %d,\nthe beginning time from %d and the end time from %d.\n', nmeetings, has.day, has.begin, has.end))

png('smart.png', width = 2400, height = 1800, res = 200)
barplot(c(nmeetings, has.day, has.begin, has.end), axes = F, main = 'How complete is the parse?')
axis(1, at = 1:4, labels = c('Total meetings', 'With day of week', 'With begin time', 'With end time'))
axis(2)
dev.off()
