"""
File: insthashtale.py
Language: Python3
Authors : rps7183@cs.rit.edu  Ruzan Sasuri
          av2833@cs.rit.edu   Akash Venkatachalam
Description : A code to create a hash table with the number of occurrences based on the words in a file, and to print
              the number of collisions, probes and the word which occurs the maximum amount of times, for different hash
              fuctions and maximum load levels.
"""
import re


class Entry:
    """
    The node used for the hash table. Contains a key and the number of occurrences of the word as its value.
    """
    __slots__ = 'key', 'value'

    def __init__(self, key, value):
        """
        Initializes the Node.
        :pre: The value should be greater than zero.
        :param key: The word found.
        :param value: The number of occurrences of the word. Default value is 1.
        """
        self.key = key
        self.value = value


class Hashes:
    """
    The Hash table used to store the words and its occurrences.
    """
    __slots__ = 'table', 'maxload', 'size', 'sizecap', 'collisions', 'probes', 'hashfn'

    def __init__(self, hashfunc, load=0.7, inisize=100):
        """
        Initializes the hash map, based on its hash function, maximum load and initial size.
        :pre: The load should be a real number between 0 and 1. The initial size should be greater than zero.
        :param hashfunc: The hash function being used by the hash map.
        :param load: The maximum number of elements permitted before the size of the hash map is increased.
        :param inisize: The initial size of the hash map.
        """
        self.maxload = load
        self.hashfn = hashfunc
        self.size = 0
        self.collisions = 0
        self.probes = 0
        self.sizecap = inisize
        self.table = [None for _ in range(inisize)]

    def put(self, key, value=1):
        """
        Adds a word to the hash map based on its key.
        :pre: Key should be a valid  input to the hash function.
        :param key: The entry to be added to the hash function.
        :param value:
        :return: None.
        """
        hashvalue = self.hashfn(key) % self.sizecap
        first = True
        while self.table[hashvalue] is not None and self.table[hashvalue].key != key:
            hashvalue = (hashvalue + 1)
            if first:
                self.collisions += 1
                first = False
            self.probes += 1
            if hashvalue >= self.sizecap:
                hashvalue = 0
        if self.table[hashvalue] is None:
            self.size += 1
        if self.table[hashvalue] is not None and self.table[hashvalue].key == key:
            self.table[hashvalue].value += 1
        else:
            self.table[hashvalue] = Entry(key, value)
        if self.size / self.sizecap > self.maxload:
            oldtable = self.table
            self.sizecap *= 2
            self.size = 0
            self.table = [None for _ in range(self.sizecap)]
            for item in oldtable:
                if item is not None:
                    self.put(item.key, item.value)

    def _find(self, key):
        """
        A helper function to find the index in the hash map where the key occurs.
        :param key: The key to be found within the hash map.
        :return: The index of the key in the hash map.
        """
        hashvalue = self.hashfn(key, self.sizecap) % self.sizecap
        if self.table[hashvalue] is not None:
            self.collisions += 1
        while self.table[hashvalue] is not None and self.table[hashvalue].key != key:
            hashvalue = (hashvalue + 1)
            self.probes += 1
            if hashvalue >= self.sizecap:
                hashvalue = 0
        return hashvalue

    def get(self, key):
        """
        Returns the number of occurrences of a particular word.
        :param key: The word to be searched.
        :return: The value of the word or None if it does not exist.
        """
        hashvalue = self._find(key)
        if self.table[hashvalue].key == key:
            return self.table[hashvalue].value
        else:
            print(key, 'not found')

    def __contains__(self, key):
        """
        Checks if a particular item exists in the hash map.
        :param key: The key to be found.
        :return: True if the ke exists, false otherwise.
        """
        hashvalue = self._find(key)
        if self.table[hashvalue].key == key:
            return True
        else:
            return False

    def __iter__(self):
        """
        Creates an iterator for the hash map, using it's table.
        :return: Returns the table as an iterator.
        """
        return iter(self.table)


def hash_first(value):
    """
    The first hash function, which converts each character's ascii value into a binary form, treats the binary as a
    decimal value, and adds them for all the characters.
    :param value: The value whose hash value has to be found.
    :return: The hash value.
    """
    x = 0
    for character in value:
        x += int(bin(ord(character))[2:])
    return x


def hash_second(value):
    """
    The second hash function which multiplies the ascii value of each character by 128 raised to the power of its index.
    :param value: The value whose hash value has to be found.
    :return: The hash value.
    """
    hashvalue = 0
    for i in range(len(value)):
        hashvalue += ord(value[i]) * pow(128, i)
    return hashvalue


def file_check(file, perm):
    """
    Checks if the file exists and opes it.
    :param file: The name of the file.
    :param perm: The permission to be given to the file.
    :return: The file handler.
    """
    try:
        f = open(file, perm)
        return f
    except FileNotFoundError:
        print("File", file, "does not exist...")
        exit()


def max_element(h):
    """
    Finds the word with the maximum number of occurrences within a hash map.
    :param h: The hash map used.
    :return: The node with the maximum number of occurrences.
    """
    maximum = None
    for item in h:
        if item is not None:
            if maximum is None:
                maximum = item
            elif item.value > maximum.value:
                maximum = item
    return maximum


def main():
    """
    The main function. Takes in a file, creates 9 hash maps bases on 3 hash functions and 3 max loads. It then prints
    the number of probes, collisions, and the most occurring word.
    :return: None.
    """
    hf = Hashes(hash_first)
    hs = Hashes(hash_second)
    hi = Hashes(hash)
    hf2 = Hashes(hash_first, load=0.8)
    hs2 = Hashes(hash_second, load=0.8)
    hi2 = Hashes(hash, load=0.8)
    hf3 = Hashes(hash_first, load=0.9)
    hs3 = Hashes(hash_second, load=0.9)
    hi3 = Hashes(hash, load=0.9)

    file = input('Enter the file: ')
    fh = file_check(file, 'r')
    nw = 0
    for line in fh:
        words = re.split('\W+', line)
        for word in words:
            if word != '':
                nw += 1
                word = word.lower()
                hf.put(word)
                hs.put(word)
                hi.put(word)
                hf2.put(word)
                hs2.put(word)
                hi2.put(word)
                hf3.put(word)
                hs3.put(word)
                hi3.put(word)

    print('For load =', hi.maxload)
    print()
    print('Inbuilt Function')
    print('collisions =', hi.collisions)
    print('probes =', hi.probes)
    print()
    print('First Function')
    print('collisions =', hf.collisions)
    print('probes =', hf.probes)
    print()
    print('Second Function')
    print('collisions =', hs.collisions)
    print('probes =', hs.probes)
    print()
    print()

    print('For load =', hi2.maxload)
    print()
    print('Inbuilt Function')
    print('collisions =', hi2.collisions)
    print('probes =', hi2.probes)
    print()
    print('First Function')
    print('collisions =', hf2.collisions)
    print('probes =', hf2.probes)
    print()
    print('Second Function')
    print('collisions =', hs2.collisions)
    print('probes =', hs2.probes)
    print()
    print()

    print('For load =', hi3.maxload)
    print()
    print('Inbuilt Function')
    print('collisions =', hi3.collisions)
    print('probes =', hi3.probes)
    print()
    print('First Function')
    print('collisions =', hf3.collisions)
    print('probes =', hf3.probes)
    print()
    print('Second Function')
    print('collisions =', hs3.collisions)
    print('probes =', hs3.probes)
    print()
    maximum = max_element(hi)
    print('The word with the most number of occurrences is \'', maximum.key, '\' which occurs', maximum.value, 'times')

if __name__ == '__main__':
    main()
