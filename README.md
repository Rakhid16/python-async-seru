# How to :
1. Pull/clone this repository
2. Execute this commands
```
$ pip3 install -r requirements.txt
$ python3 create_db.py
```
3. Execute each file on each scenario

# Illustration
<img src="https://i.imgur.com/4gd7Z5Q.jpg">

# Benchmark Results

## API Scenario
| Method | Seconds  |
| :---:   | :-: |
| Synchronous | 131 or 199 |
| Multithread | 9.5 |
| Multiprocess | 8.6 |
| Asynchronous | 2.7 |

## DB Scenario
| Rows | Synchronous | Asynchronous |
| :---:   | :-: | :-: |
| 43104 | 6.6 s | - |
| 86208 | - | 2 s |
| 172416 | 26 s | - |
| 344832 | - | 8.9 s |
| 689664 | 102 s | - |
| 1379328 | - | 57.2 s |

## Multiprocess with Sync/Async Scenario
| Method | Seconds  |
| :---:   | :-: |
| Synchronous | 7.9 |
| Asynchronous | 6.7 |

## Multithread with Sync/Async Scenario
| Method | Seconds  |
| :---:   | :-: |
| Synchronous | 9.0 |
| Asynchronous | 8.8 |