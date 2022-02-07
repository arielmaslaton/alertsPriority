# Alerts Priority

'alertsPriority' is an algorithm design to scan a file containing alerts from various sources,
And output a configured amount of cherry-picked alert specified by configuration priority rule map.

## Description

An “alert” is an object with the following keys: Alert ID, Type, Subtype, Title, and FoundDate.

Some alerts are more important than others and are classified according to the rule map by priority, 1 - the highest priority and 6 - lowest.

Beside the main file, in the project you will find the following files:

'AlertProperties.py' - the mentioned priority rules map

'AlertExamples.py' - containing alert examples

'SearchPatternAlgorithm.py' - a search algorithm used to find patter within a given txt

## Getting Started
My approach taken is as follows:

First, the algorithem iterate over the alerts file and for each alert:

Iterates over the priority rules map, from the highest priority to the lowest and try to find a match.

The match is done first to 'type' and 'subtype',then try to match the titles.

Since a title identifier could be a subset of an alert identifier a Knuth–Morris–Pratt algorithm was used to find a match.
Boyer-Moore algorithm or suffix tree was considered as well but for our purpose Knuth–Morris–Pratt algorithm seems to be the most efficient in speed and complexity - O(n)

After a full match is done, the results: Alert Priority Level, Alert ID, and alert timestamp are set in a list.

The list size is the amount of priority levels within the priority rule map (meaning 6 in our case - but if the priority levels will increase so does the list size)

Each element of the list (meaning priority level) contains a dictionary with the key being an alert ID and the value the timestamp

The next step was to sort the timestamps in order to collect the most recent (highest priority) alerts.
In order to do so a ciso8601 was used to parse the timestamp (ciso8601 seems to be the fastest way to parse a timestamp).
Then it converts the timestamp to unix time for fast comparison.

A reverse sort is done using a specific sorted() function in order to have first the most recent alerts for each priority (in recent python versions the dictionary insertion order is kept)

After the sorting is done a list containing all the matched alerts by priority level sorted by time is received.

Next the algorithm takes the first configured number of cherry-picked alerts (4 in our case) starting from the highest priority, 
and insert them into a list(as well as print the results)

## Complexity
Complexity calculation:
O(n) for Knuth–Morris–Pratt title subset search +
O(n*logn) for timestamp sorting +
O(mn) for iterating each alert over all priorities (worst case)

### Dependencies

* The algorithm is written in Python language, and it is advised to use version 3.7 and up
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
