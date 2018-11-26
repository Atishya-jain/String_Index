# String_Index
This repository contains implementation of prefix trees data structure to support operations like search all strings given a prefix or suffix. This data structure is optimised for string queries and is efficient for parallel queries. It is certain that it would not lead to any inconsistencies 

# Implementation Details
I have maintained 2 trees. One is the standard prefix tree and other is the prefix tree over inverted strings (Let me call that suffix tree). This approach helps in handling search queries for both prefix and suffix searches.
There are 2 classes StringIndex and Result. StringIndex is the main datastructure with its endpoints as:
   - StringsWithPrefix: This method takes in the string as input and returns all the strings whose prefix is the string. 
   - StringsWithSuffix
   - Insert

# Assumptions
1. 

# Methods and runtimes

# Limitations/ Tradeoff

# Usage
    
# Author
 - Atishya Jain
