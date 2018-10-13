#!/usr/bin/env python3 
# Instructors: Dr. Scott Rixner, Dr. Joe Warren
# Course: Python Data Visualization, University of Michigan, Coursera.
#

NUM_ROWS = 5
NUM_COLS = 9

def nested_dict_matrix(NUM_ROWS, NUM_COLS):
    matrix = {}

    for row in range(NUM_ROWS):
        new_row = {}
        for col in range(NUM_COLS):
            new_row[col] = (row * col)

        matrix[row] = new_row

    return matrix

def nested_list_matrix(NUM_ROWS, NUM_COLS):
    matrix = []

    for row in range(NUM_ROWS):
        new_row = []
        for col in range(NUM_COLS):
            new_row.append(row * col)

        matrix.append(new_row)

    return matrix

def pprint_matrix(matrix):
    NUM_ROWS = len(matrix)
    NUM_COLS = len(matrix[0])

    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            print("{:3}".format(matrix[row][col]), end = " ")
        print()

def matrix_trace(matrix):
    trace = 0
    NUM_ROWS = len(matrix)
    NUM_COLS = len(matrix[0])
    
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if col == row:
                trace += matrix[row][col]

    return trace

trace = matrix_trace(nested_dict_matrix(25, 25))
print(trace)

matrix = nested_dict_matrix(5,9)

print(matrix)
pprint_matrix(matrix)

