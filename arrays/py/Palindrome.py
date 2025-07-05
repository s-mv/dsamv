from Helper import Helper


class Solution:
    def solution(self, input_str):
        for i in range(len(input_str) // 2):
            if input_str[i] != input_str[-(i + 1)]:
                return False
        return True

Helper.test(Solution())
