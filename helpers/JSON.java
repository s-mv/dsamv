package helpers;

import java.util.*;

// I really want to name this JSONMV
public class JSON {

  public abstract static class JSONValue {
    public enum Type {
      NULL, BOOLEAN, NUMBER, STRING, ARRAY, OBJECT
    }

    public abstract Type getType();

    public boolean asBoolean() {
      throw new UnsupportedOperationException("Not a boolean!");
    }

    public double asNumber() {
      throw new UnsupportedOperationException("Not a number!");
    }

    public String asString() {
      throw new UnsupportedOperationException("Not a string!");
    }

    public List<JSONValue> asArray() {
      throw new UnsupportedOperationException("Not an array!");
    }

    public Map<String, JSONValue> asObject() {
      throw new UnsupportedOperationException("Not an object!");
    }
  }

  public static class JSONNull extends JSONValue {
    @Override
    public Type getType() {
      return Type.NULL;
    }

    @Override
    public String toString() {
      return "null";
    }
  }

  public static class JSONBoolean extends JSONValue {
    private final boolean value;

    public JSONBoolean(boolean value) {
      this.value = value;
    }

    @Override
    public Type getType() {
      return Type.BOOLEAN;
    }

    @Override
    public boolean asBoolean() {
      return value;
    }

    @Override
    public String toString() {
      return Boolean.toString(value);
    }
  }

  public static class JSONNumber extends JSONValue {
    private final double value;

    public JSONNumber(double value) {
      this.value = value;
    }

    @Override
    public Type getType() {
      return Type.NUMBER;
    }

    @Override
    public double asNumber() {
      return value;
    }

    @Override
    public String toString() {
      return Double.toString(value);
    }
  }

  public static class JSONString extends JSONValue {
    private final String value;

    public JSONString(String value) {
      this.value = value;
    }

    @Override
    public Type getType() {
      return Type.STRING;
    }

    @Override
    public String asString() {
      return value;
    }

    @Override
    public String toString() {
      return "\"" + value + "\"";
    }
  }

  public static class JSONArray extends JSONValue {
    private final List<JSONValue> values;

    public JSONArray(List<JSONValue> values) {
      this.values = values;
    }

    @Override
    public Type getType() {
      return Type.ARRAY;
    }

    @Override
    public List<JSONValue> asArray() {
      return values;
    }

    @Override
    public String toString() {
      return values.toString();
    }
  }

  public static class JSONObject extends JSONValue {
    private final Map<String, JSONValue> values;

    public JSONObject(Map<String, JSONValue> values) {
      this.values = values;
    }

    @Override
    public Type getType() {
      return Type.OBJECT;
    }

    @Override
    public Map<String, JSONValue> asObject() {
      return values;
    }

    @Override
    public String toString() {
      return values.toString();
    }
  }

  public static class Parser {
    private final String input;
    private int pos;

    public Parser(String input) {
      this.input = input;
      this.pos = 0;
    }

    public JSONValue parse() {
      JSONValue value = parseValue();
      skipWhitespace();
      if (pos != input.length()) {
        throw new RuntimeException("Unexpected characters at end of JSON!");
      }
      return value;
    }

    private JSONValue parseValue() {
      skipWhitespace();
      char c = peek();

      switch (c) {
        case '"':
          return new JSONString(parseString());
        case '{':
          return parseObject();
        case '[':
          return parseArray();
        case 't':
          expect("true");
          return new JSONBoolean(true);
        case 'f':
          expect("false");
          return new JSONBoolean(false);
        case 'n':
          expect("null");
          return new JSONNull();
        default:
          if (c == '-' || Character.isDigit(c)) {
            return new JSONNumber(parseNumber());
          }
          throw new RuntimeException("Unexpected character: " + c + "!");
      }
    }

    private JSONObject parseObject() {
      expect('{');
      Map<String, JSONValue> map = new LinkedHashMap<>();
      skipWhitespace();
      if (peek() == '}') {
        consume();
        return new JSONObject(map);
      }
      while (true) {
        String key = parseString();
        skipWhitespace();
        expect(':');
        JSONValue value = parseValue();
        map.put(key, value);
        skipWhitespace();
        char c = consume();
        if (c == '}')
          break;
        if (c != ',')
          throw new RuntimeException("Expected ',' or '}' in object!");
      }
      return new JSONObject(map);
    }

    private JSONArray parseArray() {
      expect('[');
      List<JSONValue> list = new ArrayList<>();
      skipWhitespace();
      if (peek() == ']') {
        consume();
        return new JSONArray(list);
      }
      while (true) {
        list.add(parseValue());
        skipWhitespace();
        char c = consume();
        if (c == ']')
          break;
        if (c != ',')
          throw new RuntimeException("Expected ',' or ']' in array!");
      }
      return new JSONArray(list);
    }

    private double parseNumber() {
      int start = pos;
      if (peek() == '-')
        pos++;
      while (pos < input.length() && Character.isDigit(input.charAt(pos)))
        pos++;
      if (pos < input.length() && input.charAt(pos) == '.') {
        pos++;
        while (pos < input.length() && Character.isDigit(input.charAt(pos)))
          pos++;
      }
      if (pos < input.length() && (input.charAt(pos) == 'e' || input.charAt(pos) == 'E')) {
        pos++;
        if (input.charAt(pos) == '+' || input.charAt(pos) == '-')
          pos++;
        while (pos < input.length() && Character.isDigit(input.charAt(pos)))
          pos++;
      }
      return Double.parseDouble(input.substring(start, pos));
    }

    private String parseString() {
      expect('"');
      StringBuilder sb = new StringBuilder();
      while (true) {
        char c = consume();
        if (c == '"')
          break;
        if (c == '\\') {
          c = consume();
          switch (c) {
            case '"':
              sb.append('"');
              break;
            case '\\':
              sb.append('\\');
              break;
            case '/':
              sb.append('/');
              break;
            case 'b':
              sb.append('\b');
              break;
            case 'f':
              sb.append('\f');
              break;
            case 'n':
              sb.append('\n');
              break;
            case 'r':
              sb.append('\r');
              break;
            case 't':
              sb.append('\t');
              break;
            case 'u':
              sb.append("\\u");
              for (int i = 0; i < 4; i++)
                sb.append(consume());
              break;
            default:
              throw new RuntimeException("Invalid escape character!");
          }
        } else {
          sb.append(c);
        }
      }
      return sb.toString();
    }

    private void skipWhitespace() {
      while (pos < input.length() && Character.isWhitespace(input.charAt(pos))) {
        pos++;
      }
    }

    private char peek() {
      skipWhitespace();
      return input.charAt(pos);
    }

    private char consume() {
      return input.charAt(pos++);
    }

    private void expect(char expected) {
      char c = consume();
      if (c != expected) {
        throw new RuntimeException("Expected '" + expected + "' but got '" + c + "'!");
      }
    }

    private void expect(String expected) {
      for (char c : expected.toCharArray()) {
        expect(c);
      }
    }
  }

  public static void main(String[] args) {
    String json = """
            {
                "name": "Jane",
                "age": 28,
                "married": false,
                "hobbies": ["reading", "travel", "code"],
                "address": {
                    "city": "NYC",
                    "zip": "10001"
                },
                "gpa": 3.75,
                "spouse": null
            }
        """;

    try {
      Parser parser = new Parser(json);
      JSONValue root = parser.parse();

      System.out.println("Parsed JSON:");
      System.out.println(root);

      if (root.getType() == JSONValue.Type.OBJECT) {
        Map<String, JSONValue> obj = root.asObject();
        System.out.println("Name: " + obj.get("name").asString());
        System.out.println("GPA: " + obj.get("gpa").asNumber());
      }
    } catch (Exception e) {
      System.err.println("Parse error: " + e.getMessage());
    }
  }
}
