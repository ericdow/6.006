#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###

# Produces hash values for a rolling sequence.
class RollingHash:
    def __init__(self, s):
        self.HASH_BASE = 7
        self.seqlen = len(s)
        n = self.seqlen - 1
        h = 0
        for c in s:
            h += ord(c) * (self.HASH_BASE ** n)
            n -= 1
        self.curhash = h

    # Returns the current hash value.
    def current_hash(self):
        return self.curhash

    # Updates the hash by removing previtm and adding nextitm.
    # Returns the updated hash value.
    def slide(self, previtm, nextitm):
        self.curhash = (self.curhash * self.HASH_BASE) + ord(nextitm)
        self.curhash -= ord(previtm) * (self.HASH_BASE ** self.seqlen)
        return self.curhash

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.d = dict()
        for pair in pairs:
            self.put(pair[0], pair[1])
    # Associates the value v with the key k.
    def put(self, k, v):
        try:
            l = self.d[k]
            l.append(v)
        except KeyError:
            self.d[k] = []
            self.d[k].append(v)
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        try:
            return self.d[k]
        except KeyError:
            return []

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    try:
        subseq = ''
        n = 0
        while True:
            while len(subseq) < k:
                subseq += seq.next()
            if n == 0:
                rh = RollingHash(subseq)
            else:
                rh.slide(cprev, subseq[-1])
            cprev = subseq[0]
            yield n, subseq, rh.current_hash()
            subseq = subseq[1:]
            n += 1
    except StopIteration:
        return

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    try:
        n = 0
        while True:
            # Grab the first k nucleotides
            subseq = ''
            while len(subseq) < k:
                subseq += seq.next()
            rh = RollingHash(subseq)
            yield n, subseq, rh.current_hash()
            # Skip the next m - k nucleotides
            for i in range(0, m-k):
                seq.next()
            n += m
    except StopIteration:
        return

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    # Build a multi-dict with the values from sequence a
    md = Multidict()
    for pos_a, subseq_a, hash_a in intervalSubsequenceHashes(a, k, m):
        md.put(hash_a, (pos_a, subseq_a))
    for pos_b, subseq_b, hash_b in subsequenceHashes(b, k):
        matches = md.get(hash_b)
        for (pos_a, subseq_a) in matches:
            if subseq_a != subseq_b:
                continue
            yield (pos_a,pos_b)
    return 

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
