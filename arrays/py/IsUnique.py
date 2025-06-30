from Helper import Helper


class Solution:
    def solution(self, input_str):
        seen = set()
        for char in input_str:
            if char in seen:
                return False
            seen.add(char)
        return True


Helper.test(Solution())
