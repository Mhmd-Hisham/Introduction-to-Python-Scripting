#!/usr/bin/env python3
# Instructors: Dr. Scott Rixner, Dr. Joe Warren
# Course: Python Data Visualization, University of Michigan, Coursera.
#

"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

IDENTICAL = -1

def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """

    len1 = len(line1)
    len2 = len(line2)
    
    minimum = min(len1, len2)
    
    # check the short one first.
    for idx in range(minimum):
        if line1[idx] != line2[idx]:
            return idx

    # if one is a prefix of the other
    if len1 != len2:
        return 0 if (minimum == 0) else abs(len1 - len2)+2

    return IDENTICAL

def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """
    # checking newliens
    if ('\n' in line1) or ('\n' in line2):
        return ""

    # checking index
    if (idx > min(len(line1), len(line2))) or (idx == IDENTICAL):
        return ""

    return line1 + '\n' + '='*(idx) + '^' + '\n' + line2 + '\n'

def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    len1 = len(lines1)
    len2 = len(lines2)

    minimum = min(len1, len2)
    # the shorter first.
    for line_idx in range(minimum):
        idx = singleline_diff(lines1[line_idx], lines2[line_idx])
        if idx != IDENTICAL:
            return (line_idx, idx)
    
    if len1 != len2:
        return (0 if minimum == 0 else abs(len1-len2)+1, 0)

    return (IDENTICAL, IDENTICAL)

def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    data = open(filename, "rt")
    lines = []
    for line in data:
        lines.append(line.strip())
    
    data.close()
    
    return lines

def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    
    lines1 = get_file_lines(filename1)
    lines2 = get_file_lines(filename2)
    
    line_idx, idx = multiline_diff(lines1, lines2)
    if (line_idx, idx) == (IDENTICAL, IDENTICAL):
        return "No differences\n"

    lines1 = lines1 if len(lines1) > 0 else [""]
    lines2 = lines2 if len(lines2) > 0 else [""]

    diff = singleline_diff_format(lines1[line_idx], lines2[line_idx], idx)
    return "Line %s:\n"%(line_idx) + diff
    

