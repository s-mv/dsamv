package arrays.java;

import java.util.*;

public class IsUnique {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String line = scanner.nextLine().trim();
        Set<Character> seen = new HashSet<>();

        for (char c : line.toCharArray()) {
            if (seen.contains(c)) {
                System.out.println("false");
                System.exit(0);
            }
            seen.add(c);
        }

        System.out.println("true");
        scanner.close();
    }
}
