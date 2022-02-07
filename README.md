# Alerts Priority

'alertsPriority' is an algorithm design to scan a file contaning alerts from various sources,
And output a configured amount of cherry-picked alert specified by configuration priority rule map.

## Description

An “alert” is an object with the following keys: Alert ID, Type, Subtype, Title, and FoundDate.

Some alerts are more important than others and are classified according to the rule map by priority, 1 - highest priority and 6 - lowest.

Beside the main file, in the project you will find the following files:

'AlertProperties.py' - the mentioned priority rules map

'AlertExamples.py' - containing alert examples

'SearchPatternAlgorithm.py' - a search algorithm used to find patter within a givent txt

## Getting Started
The aproach taken is as follows:

First, we iterate of the alerts file and for each alert:

We iterate over the priority rules map, from the highest priority to the lowest and try to find a match.

The match is searched first by the titles (instead of matching type and subtype - since title is more likely to fail.

After any match to one of the 'titles identifiers' is found, we try to find a type and subtype match



## Complexity


## Getting Started

### Dependencies

* The algorythem is written in Python language and it is advise to use version 3.7 and up
* ciso8601 package is needed in order to parse timestamp in an efficiant way
* pip is needed to install ciso8601


## Installation

<div class="termy">
  pip install

```console
$ python -m pip install quux
...
Installing collected packages baz, bar, foo, quux

$ python -m pip install bar
...
Installing collected packages foo, baz, bar
  
```
  
  ciso8601 install
  ```console
$ pip install ciso8601
---> 100%
  
  ```

### Executing program

* run the main.py main function


## Authors

Ariel Maslaton  
[arielmaslaton@gmail.com](https://github.com/arielmaslaton/)


## License

This project is not licensed
