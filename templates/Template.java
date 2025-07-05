// add `package <type>.java;` here if this fails

import java.util.*;

public class Template {
    public static void main(String[] args) {
        // you have to scan input to read it
        // this example runs code equivalent to arrays/java/IsUnique.java
        Scanner scanner = new Scanner(System.in);
        String line = scanner.nextLine().trim();
        Set<Character> seen = new HashSet<>();

        for (char c : line.toCharArray()) {
            if (seen.contains(c)) {
                // print the output - this will be read by the tests
                System.out.println("false");
                System.exit(0);
            }
            seen.add(c);
        }

        // print the output - this will be read by the tests
        System.out.println("true");
        scanner.close();
    }
}
