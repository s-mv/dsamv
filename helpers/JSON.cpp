#include "JSON.hpp"

#include <cctype>
#include <iostream>
#include <stdexcept>

JSONMV::JSONValue::JSONValue() : type(JSONType::json_null) {}
JSONMV::JSONValue::JSONValue(std::nullptr_t) : type(JSONType::json_null) {}
JSONMV::JSONValue::JSONValue(bool value)
    : type(JSONType::json_bool), boolValue(value) {}
JSONMV::JSONValue::JSONValue(double value)
    : type(JSONType::json_num), numberValue(value) {}
JSONMV::JSONValue::JSONValue(const std::string &value)
    : type(JSONType::json_str) {
  stringValue = new std::string(value);
}
JSONMV::JSONValue::JSONValue(JSONArray &&value) : type(JSONType::json_array) {
  arrayValue = new JSONArray(std::move(value));
}
JSONMV::JSONValue::JSONValue(JSONObject &&value) : type(JSONType::json_object) {
  objectValue = new JSONObject(std::move(value));
}

JSONMV::JSONValue::~JSONValue() { cleanUp(); }

JSONMV::JSONValue::JSONValue(const JSONValue &other) : type(other.type) {
  switch (type) {
  case JSONType::json_null:
    break;
  case JSONType::json_bool:
    boolValue = other.boolValue;
    break;
  case JSONType::json_num:
    numberValue = other.numberValue;
    break;
  case JSONType::json_str:
    stringValue = new std::string(*other.stringValue);
    break;
  case JSONType::json_array:
    arrayValue = new JSONArray(*other.arrayValue);
    break;
  case JSONType::json_object:
    objectValue = new JSONObject(*other.objectValue);
    break;
  }
}

JSONMV::JSONValue::JSONValue(JSONValue &&other) noexcept : type(other.type) {
  switch (type) {
  case JSONType::json_null:
    break;
  case JSONType::json_bool:
    boolValue = other.boolValue;
    break;
  case JSONType::json_num:
    numberValue = other.numberValue;
    break;
  case JSONType::json_str:
    stringValue = other.stringValue;
    other.stringValue = nullptr;
    break;
  case JSONType::json_array:
    arrayValue = other.arrayValue;
    other.arrayValue = nullptr;
    break;
  case JSONType::json_object:
    objectValue = other.objectValue;
    other.objectValue = nullptr;
    break;
  }
  other.type = JSONType::json_null;
}

template <typename T> T JSONMV::JSONValue::toNative() const {
  switch (type) {
  case JSONType::json_bool:
    if constexpr (std::is_same_v<T, bool>) {
      return boolValue;
    }
    break;
  case JSONType::json_num:
    if constexpr (std::is_same_v<T, double>) {
      return numberValue;
    }
    break;
  case JSONType::json_str:
    if constexpr (std::is_same_v<T, std::string>) {
      return *stringValue;
    }
    break;
  case JSONType::json_array:
    if constexpr (std::is_same_v<T, JSONArray>) {
      return *arrayValue;
    }
    break;
  case JSONType::json_object:
    if constexpr (std::is_same_v<T, JSONObject>) {
      return *objectValue;
    }
    break;
  default:
    throw std::runtime_error("ERROR: Unsupported type!");
  }

  throw std::runtime_error("ERROR: Type mismatch... or something!");
}

JSONMV::JSONValue &JSONMV::JSONValue::operator=(JSONValue &&other) noexcept {
  if (this != &other) {
    cleanUp();
    type = other.type;
    switch (type) {
    case JSONType::json_null:
      break;
    case JSONType::json_bool:
      boolValue = other.boolValue;
      break;
    case JSONType::json_num:
      numberValue = other.numberValue;
      break;
    case JSONType::json_str:
      stringValue = other.stringValue;
      other.stringValue = nullptr;
      break;
    case JSONType::json_array:
      arrayValue = other.arrayValue;
      other.arrayValue = nullptr;
      break;
    case JSONType::json_object:
      objectValue = other.objectValue;
      other.objectValue = nullptr;
      break;
    }
    other.type = JSONType::json_null;
  }
  return *this;
}

void JSONMV::JSONValue::cleanUp() {
  switch (type) {
  case JSONType::json_str:
    delete stringValue;
    break;
  case JSONType::json_array:
    delete arrayValue;
    break;
  case JSONType::json_object:
    delete objectValue;
    break;
  default:
    break;
  }
}

void JSONMV::skipWhitespace() {
  while (pos < source.length() && std::isspace(source[pos]))
    pos++;
}

char JSONMV::peek() {
  skipWhitespace();
  return pos < source.length() ? source[pos] : '\0';
}

char JSONMV::consume() {
  skipWhitespace();
  return pos < source.length() ? source[pos++] : '\0';
}

void JSONMV::expect(char expected) {
  char c = consume();
  if (c != expected) {
    throw std::runtime_error("ERROR: Expected '" + std::string(1, expected) +
                             "', got '" + std::string(1, c) + "'!");
  }
}

std::string JSONMV::parseString() {
  expect('"');
  std::string result;
  while (pos < source.length() && source[pos] != '"') {
    if (source[pos] == '\\') {
      pos++;
      if (pos >= source.length())
        throw std::runtime_error("ERROR: Unterminated escape sequence!");
      switch (source[pos]) {
      case '"':
        result += '"';
        break;
      case '\\':
        result += '\\';
        break;
      case '/':
        result += '/';
        break;
      case 'b':
        result += '\b';
        break;
      case 'f':
        result += '\f';
        break;
      case 'n':
        result += '\n';
        break;
      case 'r':
        result += '\r';
        break;
      case 't':
        result += '\t';
        break;
      case 'u':
        result += "\\u";
        for (int i = 0; i < 4 && pos + 1 < source.length(); i++)
          result += source[++pos];
        break;
      default:
        throw std::runtime_error("ERROR: Invalid escape sequence!");
      }
    } else {
      result += source[pos];
    }
    pos++;
  }
  if (pos >= source.length())
    throw std::runtime_error("ERROR: Unterminated string!");
  pos++;
  return result;
}

double JSONMV::parseNumber() {
  size_t start = pos;
  if (source[pos] == '-')
    pos++;
  if (!std::isdigit(source[pos]))
    throw std::runtime_error("ERROR: Invalid number!");
  if (source[pos] == '0')
    pos++;
  else
    while (std::isdigit(source[pos]))
      pos++;
  if (source[pos] == '.') {
    pos++;
    if (!std::isdigit(source[pos]))
      throw std::runtime_error("ERROR: Invalid number!");
    while (std::isdigit(source[pos]))
      pos++;
  }
  if (source[pos] == 'e' || source[pos] == 'E') {
    pos++;
    if (source[pos] == '+' || source[pos] == '-')
      pos++;
    if (!std::isdigit(source[pos]))
      throw std::runtime_error("ERROR: Invalid number!");
    while (std::isdigit(source[pos]))
      pos++;
  }
  return std::stod(source.substr(start, pos - start));
}

std::shared_ptr<JSONMV::JSONValue> JSONMV::parseValue() {
  char c = peek();
  switch (c) {
  case '"':
    return std::make_shared<JSONValue>(parseString());
  case '{':
    return std::make_shared<JSONValue>(parseObject());
  case '[':
    return std::make_shared<JSONValue>(parseArray());
  case 't':
    if (source.substr(pos, 4) == "true") {
      pos += 4;
      return std::make_shared<JSONValue>(true);
    }
    break;
  case 'f':
    if (source.substr(pos, 5) == "false") {
      pos += 5;
      return std::make_shared<JSONValue>(false);
    }
    break;
  case 'n':
    if (source.substr(pos, 4) == "null") {
      pos += 4;
      return std::make_shared<JSONValue>(nullptr);
    }
    break;
  default:
    if (c == '-' || std::isdigit(c))
      return std::make_shared<JSONValue>(parseNumber());
  }
  throw std::runtime_error(
      "ERROR: Unexpected character in JSON: " + std::string(1, c) + "!");
}

JSONMV::JSONObject JSONMV::parseObject() {
  expect('{');
  JSONObject obj;
  if (peek() == '}') {
    consume();
    return obj;
  }
  while (true) {
    std::string key = parseString();
    expect(':');
    obj[key] = parseValue();
    char c = peek();
    if (c == '}') {
      consume();
      break;
    }
    if (c != ',')
      throw std::runtime_error("ERROR: Expected ',' in object!");
    consume();
  }
  return obj;
}

JSONMV::JSONArray JSONMV::parseArray() {
  expect('[');
  JSONArray arr;
  if (peek() == ']') {
    consume();
    return arr;
  }
  while (true) {
    arr.push_back(parseValue());
    char c = peek();
    if (c == ']') {
      consume();
      break;
    }
    if (c != ',')
      throw std::runtime_error("ERROR: Expected ',' in array!");
    consume();
  }
  return arr;
}

std::shared_ptr<JSONMV::JSONValue> JSONMV::parse(const std::string &jsonStr) {
  source = jsonStr;
  pos = 0;
  auto result = parseValue();
  skipWhitespace();
  if (pos != source.length())
    throw std::runtime_error("ERROR: Extra characters after JSON value!");
  return result;
}

void JSONMV::printValue(const std::shared_ptr<JSONValue> &value,
                        int indent) const {
  std::string spaces(indent * 2, ' ');
  switch (value->type) {
  case JSONType::json_null:
    std::cout << "null";
    break;
  case JSONType::json_bool:
    std::cout << (value->boolValue ? "true" : "false");
    break;
  case JSONType::json_num:
    std::cout << value->numberValue;
    break;
  case JSONType::json_str:
    std::cout << "\"" << *value->stringValue << "\"";
    break;
  case JSONType::json_object: {
    std::cout << "{\n";
    bool first = true;
    for (const auto &[key, val] : *value->objectValue) {
      if (!first)
        std::cout << ",\n";
      std::cout << spaces << "  \"" << key << "\": ";
      printValue(val, indent + 1);
      first = false;
    }
    std::cout << "\n" << spaces << "}";
    break;
  }
  case JSONType::json_array: {
    std::cout << "[\n";
    bool first = true;
    for (const auto &val : *value->arrayValue) {
      if (!first)
        std::cout << ",\n";
      std::cout << spaces << "  ";
      printValue(val, indent + 1);
      first = false;
    }
    std::cout << "\n" << spaces << "]";
    break;
  }
  }
}

bool JSONMV::isNull(const std::shared_ptr<JSONValue> &value) const {
  return value->type == JSONType::json_null;
}
bool JSONMV::getBool(const std::shared_ptr<JSONValue> &value) const {
  if (value->type != JSONType::json_bool)
    throw std::runtime_error("ERROR: Not a boolean");
  return value->boolValue;
}
double JSONMV::getNumber(const std::shared_ptr<JSONValue> &value) const {
  if (value->type != JSONType::json_num)
    throw std::runtime_error("ERROR: Not a number");
  return value->numberValue;
}
const std::string &
JSONMV::getString(const std::shared_ptr<JSONValue> &value) const {
  if (value->type != JSONType::json_str)
    throw std::runtime_error("ERROR: Not a string!");
  return *value->stringValue;
}
const JSONMV::JSONArray &
JSONMV::getArray(const std::shared_ptr<JSONValue> &value) const {
  if (value->type != JSONType::json_array)
    throw std::runtime_error("ERROR: Not an array!");
  return *value->arrayValue;
}
const JSONMV::JSONObject &
JSONMV::getObject(const std::shared_ptr<JSONValue> &value) const {
  if (value->type != JSONType::json_object)
    throw std::runtime_error("ERROR: Not an object!");
  return *value->objectValue;
}
