package helpers;

import helpers.JSON.*;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Map;

public class Helper {
  public static <T> void test(StringFunction<T> solution, String filePath) {
    try {
      String content = Files.readString(Paths.get(filePath)).replace("\uFEFF", "").trim();

      Parser parser = new Parser(content);
      JSONValue parsed = parser.parse();

      if (parsed.getType() != JSONValue.Type.OBJECT) {
        throw new RuntimeException("Expected top-level JSON object");
      }

      JSONObject jsonObject = (JSONObject) parsed;
      Map<String, JSONValue> testCases = jsonObject.asObject();

      int passed = 0;
      int total = testCases.size();

      for (Map.Entry<String, JSONValue> entry : testCases.entrySet()) {
        String input = entry.getKey();
        JSONValue expectedJson = entry.getValue();

        String expected = expectedJson.toString();
        T actualResult = solution.solution(input);
        String actual = toJsonString(actualResult);

        if (actual.equals(expected)) {
          System.out.println("[PASS] Input: \"" + input + "\" → Output: " + actual);
          passed++;
        } else {
          System.out.println("[FAIL] Input: \"" + input + "\" → Expected: " + expected + ", Got: " + actual);
        }
      }

      System.out.println("\n" + passed + "/" + total + " test cases passed.");

    } catch (IOException e) {
      System.err.println("Could not read file: " + e.getMessage());
    } catch (Exception e) {
      System.err.println("Test failed: " + e.getMessage());
      e.printStackTrace();
    }
  }

  private static String toJsonString(Object obj) {
    if (obj == null)
      return "null";
    if (obj instanceof String)
      return "\"" + obj + "\"";
    return obj.toString();
  }
}
