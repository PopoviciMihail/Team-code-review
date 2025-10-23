from collections import defaultdict
"""
Exercise 1:
FizzBuzz exercise
If a number is divisible by 3, print "Fizz" instead of the number.
If a number is divisible by 5, print "Buzz".
If a number is divisible by both 3 and 5, print "FizzBuzz".
Otherwise, print the number itself.
Implement 2 functions:
- run it for a given number
- run it for the first 100 numbers
"""

def fizz_buzz(number: int) -> None:
    print_value = ""
    if number % 3 == 0:
        print_value += "Fizz"
    if number % 5 == 0:
        print_value += "Buzz"
    if not print_value:
        print(number)
    else:
        print(print_value)


# for x in range(100):
#     fizz_buzz(x)

"""

Exercise 2:
Split `payload` into lists of size `chunk_size`
payload = [1, 7, 2, 3, 4, 5, 7]
chunk_size = 3
"""

payload = [1, 7, 2, 3, 4, 5, 7,8]
chunk_size = 3

split = [payload[x:x+chunk_size] for x in range(0,len(payload),chunk_size)]
# print(split)


"""
Exercise 3:
Get character frequency in a sentence
sentence = "This is a common interview question"
"""

sentence = "This is a common interview question"
frequency = defaultdict(list)
for x in sentence:
    frequency[x] = frequency[x]+1 if frequency[x] else 1 
print(frequency)
print(frequency['n'])