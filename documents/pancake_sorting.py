# Function for flip operation, reverses the order of the first k elements in the array
def flip(arr, k):
    arr[:k] = arr[:k][::-1]

# Function for finding the index of the largest element in the first k elements
def find_max_index(arr, k):
    return max(range(k), key=lambda i: arr[i])

# Implementation of Pancake Sorting
def pancake_sort(arr):
    n = len(arr)
    for curr_size in range(n, 1, -1):
        max_index = find_max_index(arr, curr_size)
        if max_index != curr_size - 1:
            flip(arr, max_index + 1)
            flip(arr, curr_size)
    return arr

# Test
arr = list(map(int, input().split()))
print("Original array:", arr)
print("Sorted array:", pancake_sort(arr))
