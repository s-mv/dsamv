from sys import exit

input_str = input()

for i in range(len(input_str) // 2):
    if input_str[i] != input_str[-(i + 1)]:
        print("false")
        exit(0)
print("true")
