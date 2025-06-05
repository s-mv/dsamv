#ifndef smv_dsamv_json_hpp
#define smv_dsamv_json_hpp

#include <map>
#include <memory>
#include <string>
#include <vector>

/* NOTE
 * constexpr scares me
 * ~smv
 */

class JSONMV {
public:
  struct JSONValue;

  using JSONObject = std::map<std::string, std::shared_ptr<JSONValue>>;
  using JSONArray = std::vector<std::shared_ptr<JSONValue>>;

  enum class JSONType {
    json_null,
    json_bool,
    json_num,
    json_str,
    json_array,
    json_object
  };

  struct JSONValue {
    JSONType type;

    union {
      bool boolValue;
      double numberValue;
      std::string *stringValue;
      JSONArray *arrayValue;
      JSONObject *objectValue;
    };

    JSONValue();
    JSONValue(std::nullptr_t);
    JSONValue(bool value);
    JSONValue(double value);
    JSONValue(const std::string &value);
    JSONValue(JSONArray &&value);
    JSONValue(JSONObject &&value);

    ~JSONValue(); // haha fancy

    JSONValue(const JSONValue &other);
    JSONValue(JSONValue &&other) noexcept;
    template <typename T> T toNative() const;
    JSONValue &operator=(const JSONValue &other);
    JSONValue &operator=(JSONValue &&other) noexcept;

  private:
    void cleanUp();
  };

  std::shared_ptr<JSONValue> parse(const std::string &jsonStr);
  void printValue(const std::shared_ptr<JSONValue> &value,
                  int indent = 0) const;

  bool isNull(const std::shared_ptr<JSONValue> &value) const;
  bool getBool(const std::shared_ptr<JSONValue> &value) const;
  double getNumber(const std::shared_ptr<JSONValue> &value) const;
  const std::string &getString(const std::shared_ptr<JSONValue> &value) const;
  const JSONArray &getArray(const std::shared_ptr<JSONValue> &value) const;
  const JSONObject &getObject(const std::shared_ptr<JSONValue> &value) const;

private:
  std::string source;
  int pos;

  void skipWhitespace();
  char peek();
  char consume();
  void expect(char expected);

  std::string parseString();
  double parseNumber();
  std::shared_ptr<JSONValue> parseValue();
  JSONObject parseObject();
  JSONArray parseArray();
};

#endif
