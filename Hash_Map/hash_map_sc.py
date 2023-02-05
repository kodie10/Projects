# Name: Kodie Artmayer
# OSU Email: artmayek@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/11/2022
# Description: Implementation of a Chaining Hash Map


from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Method clears the contents of the hash map.
        It does not change the underlying hash capacity
        """
        for i in range(0, self.capacity):                           #loop for length of Dynamic Array capacity
            self.buckets.set_at_index(i, LinkedList())              #set each bucket to an empty linked list
        self.size = 0                                               #set the size to 0
        return

    def get(self, key: str) -> object:
        """
        Method returns the value associated with the given key,
        if the key is not in the hash map method returns None.
        """
        hashed = self.hash_function(key)                #variable for the hash function integer
        index = hashed % self.capacity                  #index for the key
        place = self.buckets.get_at_index(index)        #variable to access the linked list class
        node = place.contains(key)                      #variable to access Slnode class
        if node is None:                                #if the node is None type
            return None                                 #nothing to get
        else:
            return node.value                           #if there is a node return the value

    def put(self, key: str, value: object) -> None:
        """
        Method updates the key/value pair in the hash map.
        """
        hashed = self.hash_function(key)                #variable for the hash function integer
        index = hashed % self.capacity                  #index for the key
        place = self.buckets.get_at_index(index)        #variable to access the linked list class
        if place.length() == 0:                         #if nothing is in the linked list
            place.insert(key, value)                    #insert the key and value in the front
            self.size += 1                              #increase the size
        elif place.contains(key):                       #if the linked list contains the key
            place.remove(key)                           #remove the old key
            place.insert(key, value)                    #insert new key value pairing
        else:
            place.insert(key, value)                    #if there is something in the list already add the new node in the front
            self.size += 1                              #increase the size
        return


    def remove(self, key: str) -> None:
        """
        Method removes the key and value from the hash map.
        """
        hashed = self.hash_function(key)                #variable for the hash function integer
        index = hashed % self.capacity                  #variable for the index
        place = self.buckets.get_at_index(index)        #variable to access linked list class
        if self.contains_key(key) is True:              #if contains key returns true
            place.remove(key)                           #call linked list remove and pass the key
            self.size -= 1                              #decrement the size
        return

    def contains_key(self, key: str) -> bool:
        """
        Method returns True if the given key is in the hash map,
        otherwise returns false
        """
        hashed = self.hash_function(key)               #variable for the hash function integer
        index = hashed % self.capacity                 #variable for the index
        place = self.buckets.get_at_index(index)       #variable to access the linked list class
        if place.contains(key) is None:                #if the linked list method returns nothing
            return False                               #does not contain key
        return True                                    #does contain key

    def empty_buckets(self) -> int:
        """
        Method returns the number of empty buckets in the
        hash table.
        """
        counter = 0                                             #counter for the empty buckets
        for i in range(0, self.capacity):                       #loop for the dynamic array
            place = self.buckets.get_at_index(i)                #variable to get linked list
            if place.length() == 0:                             #if the length of the list is 0
                counter += 1                                    #increase the counter for the empty buckets
        return counter                                          #return the number of empty buckets

    def table_load(self) -> float:
        """
        Method returns the current hash table load factor
        """
        return self.size/self.capacity                          #current size divided by current capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Method changes the capacity of the internal hash table.
        """
        if new_capacity < 1:                                    #if the new capacity is less than 1
            return                                              #do nothing
        new_buckets = DynamicArray()                            #new empty array to set up buckets later
        temp_array = DynamicArray()                             #new array to hold values
        for i in range(0, new_capacity):                        #set up the new buckets array with the proper amount of linked lists
            new_buckets.append(LinkedList())
        for i in range(0, self.capacity):                       #loop to copy data from buckets
            place = self.buckets.get_at_index(i)                #variable to access linked list class
            node = place.head                                   #variable to access SLNode class
            while node is not None:                             #while there are nodes in the linked list
                temp_array.append(node)                         #append them to the temp array
                node = node.next                                #move to the next node
        self.buckets = new_buckets                              #initialize buckets with the new buckets empty linked list array
        self.capacity = new_capacity                            #update the capacity
        self.size = 0                                           #reset the size
        for i in range(0, temp_array.length()):                 #loop for the length of the temp array
            node = temp_array.get_at_index(i)                   #variable to access nodes in temp array
            if node is not None:                                #if the node has data
                self.put(node.key, node.value)                  #call put method and pass the key and the value to put it in the bucket array
        return

    def get_keys(self) -> DynamicArray:
        """
        Method returns a Dynamic Array that contains all the keys
        stored in the hash map
        """
        return_DArray = DynamicArray()                          #create new Dynamic Array
        for i in range(0, self.capacity):                       #loop through all the buckets
            place = self.buckets.get_at_index(i)                #variable to access linked list class
            node = place.head                                   #variable to access SLNode class
            while node is not None:                             #if the node has data
                return_DArray.append(node.key)                  #append the key to the new array
                node = node.next                                #move to the next node
        return return_DArray                                    #return the new array

# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)#

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
