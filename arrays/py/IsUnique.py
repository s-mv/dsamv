from sys import exit

input_str = input()

seen = set()
for char in input_str:
    if char in seen:
        print("false")
        exit(0)
    seen.add(char)

print("true")
