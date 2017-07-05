# README
- name : Oliver Croomes

## Usage
--------

#### Running ####
1. Source python3 envrionment in scripts/venv/bin/activate
2. pip install the requriements in requirements.txt with
```
pip install -r requrirements.txt
```
3. use run.sh or run_profile.sh to run the program

#### Testing ####
```
python unittest.py
```

## Approach
-----------

I knew that reading in the data for both the batch and input files would be similar. The event streamer simply turns on and off logging depending on reading from batch or from stream. Overall how my program works is, it separates commands into three categories:
  * purchases
  * befriend
  * defriend

all of these will be represented in two data structures in datamanager.py
  * friends
  * purchases

**friends** is a graph represented by a dictionary mapping a user id to other user ids in their network.
**purchases** is a table mapping user_ids->a purchase tuple containing:
 * timestamp (float)
 * streak (integer)
 * amount (integer)

the timestamp and streak are used in the sorting algorithm heapq.merge() to join the lists of sorted items together.

for each purchase under the streaming file, the program evaluates whether or not that purchase is an anomaly by running a bfs search of depth D on the user_ID and using pythons builtin functions for sorting.

## Validation
-------------
Validation was done via a json schema. I wasn't sure the extent to which curve balls would be thrown, but I thought I could capture most errors by using schemas for each object. Regexes were used to parse the values of properties which were wrapped in strings. Format allows for non-string values. The program will halt if there are invalid lines, as in, there are no lines containing the subset of attributes in the formats required. This is because all the data is dependent upon the previous action.

EX: Gertrude unfriends a highschool student but the log was corrupted. Gertrude gets spammed with notifications about the highschoolers spending habits and is more annoyed than benefited. 

## Metagoals
------------

My overall goal was to minimize side effects as much as possible. I refactored bits of my code unpon realizing some of it caused side effects.
I also tried to use generators in as many places as possible to keep down memory size. I tried to keep things at most O(1) and O(N) where I could.  
## TODO: Small Insignificiant Optimizations
-------------------------------
- Read file lines in batch to minimize IO time
- Batch and filter friend operations to eliminate waste.
  - EX: if two people repeatedly friend and unfriend each other without transactions in their network, it's optimal to capture the state prior to a transaction between them. 

