# String_Index
This repository contains implementation of prefix trees data structure to support operations like search all strings given a prefix or suffix. This data structure is optimised for string queries and is efficient for parallel queries. It is certain that it would not lead to any inconsistencies 

# Implementation Details
I have maintained 2 trees. One is the standard prefix tree and other is the prefix tree over inverted strings (Let me call that suffix tree). This approach helps in handling search queries for both prefix and suffix searches.
There are 2 classes StringIndex and Result. StringIndex is the main datastructure with its endpoints as:
   - **StringsWithPrefix:** This method takes in the string as input and returns all the strings whose prefix is the string. For this we     search in the prefix tree. At each level it takes O(1) time to go to the next character as the children are stored in dictionary and     not arrays. Thus time for a query where there are m results will be O(m) to output the results + O(log N) i.e the max depth for the     prefix tree. (N is the total number of words in the tree)
   - **StringsWithSuffix:** Implemented in a similar way to Prefix search with the difference that all queries take place on suffix tree. Prefix search and suffix search can run in parallel.
   - **Insert:** Insert function traverses both the trees and adds the word. So O(logN)

 - **Deleting strings that were inserted before the result was made:** To differentiate the strings that are added in different queries, I have maintained a timestamp for every string. That is at each leaf along with the string, it also has a history of timestamps so that when remove action takes place, it can effectively remove only the strings that were added before it. 

 - **Duplicates Allowed:** Duplicate count is also maintained at each leaf along with the end pointer which gives us the number of same strings in the prefix/suffix tree.

 - **Result size:** Result maintains the list of strings which it gets directly when a call to prefix/suffix search was made. So simply returns the number of the strings. Once, the query to prefix/suffix search is done, it takes O(1)
 
 - **Result remove:** Result has m strings. It removes each of these strings from both the trees. It is easy to remove strings of a common prefix from the prefix tree but delete has to be done individually for each string in suffix tree. So, remove operation is O(m*logN) 

- The assumtion of concurrent reads and sequential writes results in no race conditions as datastructure can only be modified through writes but they are sequential. There will be no deadlock as the resource that is to be modified i.e the database itself can be modified in a sequential manner. So, there will be no looping of dependencies among the processes.

- There will be no livelock as in case of case of parallel reads, no one depends on another. In case of 2 writes, they occur sequentially and similarly for a read and write they too occur sequentially. That means there is never a situation where 2 processes are stuck as they need the work done by other one.

# Assumptions
1. Time complexity of prefix tree search comes out to be O(log N) if it is balanced
2. There can be concurrent reads but sequential writes. This is to remove inconsistencies that can arise due to editing of the tree while reading. This means while writing (insert/remove) no other performance can be done on the tree whereas reads can happen simultaneously. Also, writes have to wait if read is going on.
3. I came to knew about reader-writer lock libraries for python but was unsure if I can use them or not for implementing the behaviour as described for the reader-writer
4. Empty string will be treated just as another string. It will be already present when there were no inserts and after more insertions it will have a duplicate count and timestamps. So, the database already has one string in it i.e empty string. It will be returned in the strings which have prefix "" or suffix as "". It can also be removed completely just as other strings

# Limitations/ Tradeoff
1. I have maintained a uncompressed prefix tree. It can be compresses to make it even more space efficient

# Usage
 - python3 stridx.py
 - This will run various bench test cases and show the results
 - 1st bench test is addition of patterned strings to check whether if data structure is working correct
 - Then there are 2 test case evaluations, in which we add random queries with some probability where writes have somewhat lower probability. I made a wrapper function that handles the queries and returns the results.
 - We can compare the time taken for both the sequential resolution of the queries and parallel resolution to see which take more time.
 - We can also compare the end trees after both sequential and parallel query resoultion is over. If there is no query like removal of a huge amount of tree that can make a significant difference on the basis of its execution order, there should be same strings available with the trees.
 - Test cases are small for visualisation purposes. We can increase the number of random queries to test the timings of parallel and sequential operations. But for large query sets, as they are random end tree usually ends up empty as there are a lot of empty string prefix/suffix queries to delete them. One can play around with the probabilities to fix that for simulation
 
# Author
 - Atishya Jain
