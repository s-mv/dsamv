from sys import exit

# this code is equivalent to arrays/py/IsUnique.py
# read input given by the runner
input_str = input()

seen = set()
for char in input_str:
    if char in seen:
        # present output to tests by printing it
        print("false")
        exit(0)
    seen.add(char)

# present output to tests by printing it
print("true")
