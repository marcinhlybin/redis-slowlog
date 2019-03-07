# Redis slowlog viewer with sorting by execution time and date

## Installation

This script runs with Python3. Redis library is required:

```
apt install python3-redis

# or
pip install redis
```

## Usage

* By default redis-slowlog will display entire slowlog ordered by execution time descending with output trimmed to terminal width.
* Use `-d/--sort-date` to order by date.
* Use `-f/--full` to disable line trimming.
* Use `-H/--host`, `-p/--port`, `-n/--db` and `-P/--password` for Redis connection details.
* Use `-r/--reset` to reset slowlog
* Use positional argument to limit output, e.g. 10 to display top 10 entries

```
$ ./redis-slowlog.py -h

usage: redis-slowlog.py [-h] [-H HOSTNAME] [-p PORT] [-n DB] [-P PASSWORD]
                        [-f] [-r] [-d | -t]
                        [LIMIT]

Redis slowlog viewer

positional arguments:
  LIMIT                 Number of entries to display (default: None)

optional arguments:
  -h, --help            show this help message and exit
  -H HOSTNAME, --host HOSTNAME
                        Redis hostname (default: localhost)
  -p PORT, --port PORT  Redis port (default: 6379)
  -n DB, --db DB        Redis database number (default: 0)
  -P PASSWORD, --password PASSWORD
                        Redis password (default: )
  -f, --full            Do not trim command line (default: False)
  -r, --reset           Clear slowlog (default: False)
  -d                    Sort by entry date (default: time)
  -t                    Sort by execution time (default: time)
```

## Sample output

Show entire slowlog ordered by date for Redis on `localhost:6379`, database number `0`:

```
$ redis-slowlog.py -f -d

2019-03-06 02:51:39   0.63 get item_counter:it:items_for_sale
2019-03-06 02:51:53   2.48 rpush ItemCollector/v2/it/0b55b5977ef663038dc9224cff01567aa 442946210 313240104 381376312 411290614 424783476 421783866 322841237 349692811 303054674 356663013 399113062 287867920 423671291 400253963 375493735 415443543 421176256 314491028 328741112 421463529 311964210 303144183 230886184 308836181 328322764 303123743 429345194 368258385 305386887 ... (71 more arguments)
2019-03-06 02:54:51   0.10 lrange ItemCollector/v2/it/fe66919dea2dbea39db538a474b70e9b 0 -1
2019-03-06 02:54:56   0.41 rpush ItemCollector/v2/da/de6b3a3fcce44a1b4cea27d98a1a5d4f 28145131 28430359 28239836 28440436 28439375 27922494 25832177 28462048 28326877 28258184 28386198 28324335 28182434 28353678 28176878 28740988 28421243 28313435 28214599 27787533 28305586 28324871 28239423 27983453 28055604 26777442 28197376 26953015 28216788 ... (71 more arguments)
2019-03-06 02:55:09   0.41 rpush ItemCollector/v2/se/20ba08b8d08db6a412f4d3b42eddfc02 99814442 98121206 93334427 99345764 93525363 93821403 99329139 90789848 98579128 99168428 93249764 99863460 98764808 99853216 78441648 85987030 99543225 97295206 95003662 99271165 97410776 94652533 95431975 98775143 73485725 91842816 91784433 94265530 98243636 ... (71 more arguments)
[...]
```

Show slowlog for Redis running on `192.168.2.1:6000`, limit to top 5 entries:

```
$ redis-slowlog.py -H 192.168.2.1 -p 6000 5

2019-03-06 03:03:00  11.84 get ItemPages:es:Shop
2019-03-06 06:59:56  10.82 rpush ItemCollector/v2/da/fd597f57874bbbd244a302fd781942bd 28334716 28422595 28037298 28141977 27925410 28424480 28342800 28241957 284...
2019-03-06 06:17:09  10.42 expire ItemCollector/v2/it/4f401bb2b1a7d31dcddce2293bd3277e 432030
2019-03-06 05:44:14   9.76 sadd active_rating:it ["ready"]
2019-03-06 06:21:04   9.73 rpush ItemCollector/v2/it/d311eb3549242e9b6167a4543daa38b1 417533946 403498169 338410159 329296396 424474296 429354355 417612024 43038...

```
