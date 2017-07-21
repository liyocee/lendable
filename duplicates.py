"""
Function to print a duplicate number in a list

@param numbers - List of numbers

"""
def print_duplicates(numbers):
  if not isinstance(numbers, list):  # ensure it is a list
    print "numbers param must be a list"
    return
  numbers.sort() # sort the numbers in ascending order
  index = 0
  for number in numbers:
    if(index + 1 == len(numbers)):
      print numbers, "No duplicate found"
      return
    next_number = numbers[index + 1]
    if number == next_number:
      print numbers, number
      return
    index += 1

