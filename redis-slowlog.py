#!/usr/bin/env python3
# Redis slowlog viewer with sorting by execution time and date
# For usage run "redis-slowlog.py --help"

import argparse
import os
import sys
import redis
from datetime import datetime
from collections import namedtuple

parser = argparse.ArgumentParser(
    description='Redis slowlog viewer with sorting by execution time and date',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-H', '--host', metavar='HOSTNAME', dest='host', default='localhost', help='redis hostname')
parser.add_argument('-p', '--port', metavar='PORT', dest='port', default=6379, help='redis port')
parser.add_argument('-n', '--db', metavar='DB', dest='db', default=0, help='redis database number')
parser.add_argument('-P', '--password', metavar='PASSWORD', dest='password', default='', help='redis password')
parser.add_argument('-f', '--full', action='store_true', dest='full', default=False, help='do not trim slowlog entry')
parser.add_argument('-r', '--reset', action='store_true', dest='reset', default=False, help='clear slowlog')
parser.add_argument('limit', metavar='LIMIT', nargs='?', type=int, help='display this many entries')
group = parser.add_mutually_exclusive_group()
group.add_argument('-d', '--sort-date', action='store_const', dest='sort_type', const='date', help='sort by entry date')
group.add_argument('-t', '--sort-time', action='store_const', dest='sort_type', const='time', help='sort by execution time')
parser.set_defaults(sort_type='time')
args = parser.parse_args()

def parse_slowlog(slowlog):
    Entry = namedtuple('Entry', ('id', 'start_time', 'duration', 'command'))
    for entry in slowlog:
        yield Entry(
            id = entry['id'],
            start_time = datetime.fromtimestamp(entry['start_time']),
            duration = round(entry['duration'] / 1000 / 1000, 2), # in seconds
            command = entry['command'].decode())

# Terminal width
columns, rows = os.get_terminal_size(0)
command_maxlen = columns - 32

# Redis connection
r = redis.Redis(
        host=args.host,
        port=args.port,
        db=args.db,
        password=args.password,
        socket_timeout=1)

try:
    if args.reset:
        r.slowlog_reset()
        sys.exit(0)
    slowlog_len = r.slowlog_len()
    slowlog = parse_slowlog(r.slowlog_get(slowlog_len))
except Exception as e:
    print('ERROR:', str(e))
    sys.exit(1)

if args.sort_type == 'date':
    sorted_slowlog = sorted(slowlog, key=lambda x: x.id)
elif args.sort_type == 'time':
    sorted_slowlog = sorted(slowlog, key=lambda x: x.duration, reverse=True)

for entry in sorted_slowlog[:args.limit]:
    command = entry.command
    if not args.full:
        command = command[:command_maxlen].replace('\n', ' ').replace('\t', ' ')
        command += '...' if len(entry.command) > command_maxlen else ''
    print("{:%Y-%m-%d %H:%M:%S} {:>6.2f} {}".format(entry.start_time, entry.duration, command))
