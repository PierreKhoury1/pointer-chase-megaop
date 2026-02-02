## gcc -O0

| pattern | depth | loads | branches | basic_blocks | instructions |
|---|---:|---:|---:|---:|---:|
| plain | 2 | 3 | 0 | 1 | 9 |
| plain | 3 | 4 | 0 | 1 | 10 |
| plain | 5 | 6 | 0 | 1 | 12 |
| plain | 8 | 9 | 0 | 1 | 15 |
| const | 2 | 3 | 0 | 1 | 10 |
| const | 3 | 4 | 0 | 1 | 12 |
| const | 5 | 6 | 0 | 1 | 16 |
| const | 8 | 9 | 0 | 1 | 22 |
| dyn | 2 | 5 | 0 | 1 | 19 |
| dyn | 3 | 7 | 0 | 1 | 25 |
| dyn | 5 | 11 | 0 | 1 | 37 |
| dyn | 8 | 17 | 0 | 1 | 52 |
| checks | 2 | 6 | 2 | 3 | 27 |
| checks | 3 | 9 | 3 | 4 | 38 |
| checks | 5 | 15 | 5 | 6 | 60 |
| checks | 8 | 24 | 8 | 9 | 90 |

## gcc -O2

| pattern | depth | loads | branches | basic_blocks | instructions |
|---|---:|---:|---:|---:|---:|
| plain | 2 | 2 | 0 | 1 | 4 |
| plain | 3 | 3 | 0 | 1 | 5 |
| plain | 5 | 5 | 0 | 1 | 7 |
| plain | 8 | 8 | 0 | 1 | 10 |
| const | 2 | 2 | 0 | 1 | 4 |
| const | 3 | 3 | 0 | 1 | 5 |
| const | 5 | 5 | 0 | 1 | 7 |
| const | 8 | 8 | 0 | 1 | 10 |
| dyn | 2 | 2 | 0 | 1 | 6 |
| dyn | 3 | 3 | 0 | 1 | 8 |
| dyn | 5 | 5 | 0 | 1 | 12 |
| dyn | 8 | 11 | 0 | 1 | 18 |
| checks | 2 | 2 | 2 | 3 | 11 |
| checks | 3 | 3 | 3 | 3 | 15 |
| checks | 5 | 5 | 5 | 3 | 23 |
| checks | 8 | 11 | 8 | 3 | 35 |

## clang -O0

| pattern | depth | loads | branches | basic_blocks | instructions |
|---|---:|---:|---:|---:|---:|
| plain | 2 | 3 | 0 | 1 | 8 |
| plain | 3 | 4 | 0 | 1 | 9 |
| plain | 5 | 6 | 0 | 1 | 11 |
| plain | 8 | 9 | 0 | 1 | 14 |
| const | 2 | 3 | 0 | 1 | 8 |
| const | 3 | 4 | 0 | 1 | 9 |
| const | 5 | 6 | 0 | 1 | 11 |
| const | 8 | 9 | 0 | 1 | 14 |
| dyn | 2 | 5 | 0 | 1 | 12 |
| dyn | 3 | 7 | 0 | 1 | 15 |
| dyn | 5 | 11 | 0 | 1 | 21 |
| dyn | 8 | 20 | 0 | 1 | 30 |
| checks | 2 | 6 | 4 | 5 | 22 |
| checks | 3 | 9 | 6 | 7 | 31 |
| checks | 5 | 15 | 10 | 11 | 49 |
| checks | 8 | 27 | 16 | 17 | 76 |

## clang -O2

| pattern | depth | loads | branches | basic_blocks | instructions |
|---|---:|---:|---:|---:|---:|
| plain | 2 | 2 | 0 | 1 | 3 |
| plain | 3 | 3 | 0 | 1 | 4 |
| plain | 5 | 5 | 0 | 1 | 6 |
| plain | 8 | 8 | 0 | 1 | 9 |
| const | 2 | 2 | 0 | 1 | 3 |
| const | 3 | 3 | 0 | 1 | 4 |
| const | 5 | 5 | 0 | 1 | 6 |
| const | 8 | 8 | 0 | 1 | 9 |
| dyn | 2 | 2 | 0 | 1 | 5 |
| dyn | 3 | 3 | 0 | 1 | 7 |
| dyn | 5 | 5 | 0 | 1 | 11 |
| dyn | 8 | 11 | 0 | 1 | 17 |
| checks | 2 | 2 | 2 | 2 | 10 |
| checks | 3 | 3 | 3 | 2 | 14 |
| checks | 5 | 5 | 5 | 2 | 22 |
| checks | 8 | 11 | 8 | 2 | 34 |

