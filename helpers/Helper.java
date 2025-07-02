package helpers;

import helpers.JSON.*;

import java.io.IOException;
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class Helper {
  public static void test(Object solutionInstance, String filePath) {
    try {
      String content = Files.readString(Paths.get(filePath)).replace("\uFEFF", "").trim();

      Parser parser = new Parser(content);
      JSONValue parsed = parser.parse();

      if (parsed.getType() != JSONValue.Type.ARRAY) {
        throw new RuntimeException("Expected top-level JSON array");
      }

      JSONArray testCases = (JSONArray) parsed;
      List<JSONValue> testCaseList = testCases.asArray();

      int passed = 0;
      int total = testCaseList.size();

      for (JSONValue testCaseValue : testCaseList) {
        if (testCaseValue.getType() != JSONValue.Type.OBJECT) {
          throw new RuntimeException("Each test case must be a JSON object");
        }

        JSONObject testCase = (JSONObject) testCaseValue;
        Map<String, JSONValue> testCaseMap = testCase.asObject();

        if (!testCaseMap.containsKey("input") || !testCaseMap.containsKey("expected")) {
          throw new RuntimeException("Each test case must have 'input' and 'expected' fields");
        }

        JSONValue inputJson = testCaseMap.get("input");
        JSONValue expectedJson = testCaseMap.get("expected");

        if (inputJson.getType() != JSONValue.Type.ARRAY) {
          throw new RuntimeException("'input' must be a JSON array");
        }

        JSONArray inputArray = (JSONArray) inputJson;
        List<JSONValue> inputList = inputArray.asArray();
        Object[] inputArgs = new Object[inputList.size()];

        for (int i = 0; i < inputList.size(); i++) {
          inputArgs[i] = parseJsonValue(inputList.get(i));
        }

        Object expected = parseJsonValue(expectedJson);

        Method solutionMethod = findSolutionMethod(solutionInstance, inputArgs);
        solutionMethod.setAccessible(true);

        Object actualResult = solutionMethod.invoke(solutionInstance, inputArgs);
        String actual = toJsonString(actualResult);

        if (Objects.equals(actualResult, expected)) {
          System.out.println("[PASS] Input: " + Arrays.toString(inputArgs) + " → Output: " + actual);
          passed++;
        } else {
          System.out
              .println("[FAIL] Input: " + Arrays.toString(inputArgs) + " → Expected: " + expected + ", Got: " + actual);
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

  private static Method findSolutionMethod(Object solutionInstance, Object[] inputArgs) throws NoSuchMethodException {
    Method[] methods = solutionInstance.getClass().getDeclaredMethods();
    for (Method method : methods) {
      if (method.getName().equals("solution")) {
        Class<?>[] parameterTypes = method.getParameterTypes();
        if (parameterTypes.length == inputArgs.length) {
          boolean matches = true;
          for (int i = 0; i < parameterTypes.length; i++) {
            if (!parameterTypes[i].isInstance(inputArgs[i]) && !isPrimitiveMatch(parameterTypes[i], inputArgs[i])) {
              matches = false;
              break;
            }
          }
          if (matches) {
            return method;
          }
        }
      }
    }
    throw new NoSuchMethodException("No matching `solution` method found for the given inputs.");
  }

  private static boolean isPrimitiveMatch(Class<?> parameterType, Object arg) {
    if (parameterType.isPrimitive()) {
      if (parameterType == int.class && arg instanceof Integer)
        return true;
      if (parameterType == long.class && arg instanceof Long)
        return true;
      if (parameterType == double.class && arg instanceof Double)
        return true;
      if (parameterType == float.class && arg instanceof Float)
        return true;
      if (parameterType == boolean.class && arg instanceof Boolean)
        return true;
      if (parameterType == char.class && arg instanceof Character)
        return true;
      if (parameterType == byte.class && arg instanceof Byte)
        return true;
      if (parameterType == short.class && arg instanceof Short)
        return true;
    }
    return false;
  }

  private static Object parseJsonValue(JSONValue value) {
    switch (value.getType()) {
      case NUMBER:
        Number number = value.asNumber();
        if (number.doubleValue() == number.intValue()) {
          return number.intValue();
        }
        return number;
      case STRING:
        return value.asString();
      case BOOLEAN:
        return value.asBoolean();
      case ARRAY:
        List<JSONValue> array = value.asArray();
        return array.stream().map(Helper::parseJsonValue).toArray();
      case OBJECT:
        return value.asObject();
      case NULL:
        return null;
      default:
        throw new RuntimeException("Unsupported JSON value type: " + value.getType());
    }
  }

  private static String toJsonString(Object obj) {
    if (obj == null)
      return "null";
    if (obj instanceof String)
      return "\"" + obj + "\"";
    if (obj instanceof Object[])
      return Arrays.toString((Object[]) obj);
    return obj.toString();
  }
}
