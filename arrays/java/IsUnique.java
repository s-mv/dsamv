package arrays.java;

import helpers.Helper;

import java.util.HashSet;

class Solution {
    public boolean solution(String input) {
        HashSet<Character> seen = new HashSet<>();
        for (char c : input.toCharArray()) {
            if (seen.contains(c))
                return false;
            seen.add(c);
        }
        return true;
    }

    public static void main(String[] args) {
        if (args.length == 0) {
            System.err.println("Usage: java IsUnique <path-to-test-file>");
            return;
        }

        Helper.test(new Solution(), args[0]);
    }
}

public class IsUnique {
    public static void main(String[] args) {
        Solution.main(args);
    }
}