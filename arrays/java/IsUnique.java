import java.util.ArrayList;
import java.util.HashMap;

public class IsUnique {
    static HashMap<String, Boolean> tests;

    IsUnique() {
        tests = new HashMap<>();
        tests.put("you shall not pass", false);
        tests.put("you can", true);
        tests.put("you cannot", false);
        tests.put("maybe no?", true);
    }

    static boolean solution(String input) {
        ArrayList<Character> list = new ArrayList<>();
        for (int i = 0; i < input.length(); i++) {
            if (list.contains(input.charAt(i)))
                return false;
            list.add(input.charAt(i));
        }
        return true;
    }

    public static void main(String[] args) {
        tests.forEach((k, v) -> {
            boolean solution = solution(k);
            System.out.println("Running input " + k + " -> " + (solution == v ? "PASSED" : "FAILED"));
        });
    }
}
