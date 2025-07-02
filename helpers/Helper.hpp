#ifndef TEST_HELPER_HPP
#define TEST_HELPER_HPP

#include "JSON.hpp"

#include <any>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <type_traits>
#include <vector>

// Takes argument types and return type as template args
template <typename T, typename R, typename... Args> class Helper {
public:
  Helper(const std::string &filename) {
    std::ifstream file(filename);
    if (!file) {
      throw std::runtime_error("Failed to open file: " + filename);
    }

    std::string jsonContent((std::istreambuf_iterator<char>(file)),
                            std::istreambuf_iterator<char>());

    root = parser.parse(jsonContent);
    testCases = parser.getArray(root);
  }

  void runTests(T &solutionInstance) const {
    int passed = 0, total = 0;

    for (const auto &testCase : testCases) {
      if (testCase->type != JSONMV::JSONType::json_object) {
        throw std::runtime_error("Each test case must be a JSON object");
      }

      const auto &testCaseObject = parser.getObject(testCase);
      if (!testCaseObject.count("input") || !testCaseObject.count("expected")) {
        throw std::runtime_error(
            "Each test case must have 'input' and 'expected' fields");
      }

      const auto &inputArray = parser.getArray(testCaseObject.at("input"));
      const auto &expectedValue = testCaseObject.at("expected");

      std::tuple<Args...> inputArgs = parseArgs<Args...>(inputArray);
      std::any expected = parseJsonValue(expectedValue);

      std::cout << "Input: [";
      printTuple(inputArgs);
      std::cout << "] | Expected: ";
      printAny(expected);
      std::cout << " | Got: ";

      R result = std::apply(
          [&](Args... unpacked) {
            return solutionInstance.solution(unpacked...);
          },
          inputArgs);

      std::any actual = result;
      printAny(actual);

      if (compareAny(actual, expected)) {
        std::cout << " PASSED\n";
        ++passed;
      } else {
        std::cout << " FAILED\n";
      }

      ++total;
    }

    std::cout << "\nPassed " << passed << " out of " << total
              << " test cases.\n";
  }

private:
  JSONMV parser;
  std::shared_ptr<JSONMV::JSONValue> root;
  JSONMV::JSONArray testCases;

  std::any
  parseJsonValue(const std::shared_ptr<JSONMV::JSONValue> &value) const {
    switch (value->type) {
    case JSONMV::JSONType::json_bool:
      return parser.getBool(value);
    case JSONMV::JSONType::json_num: {
      double num = parser.getNumber(value);
      if (num == static_cast<int>(num))
        return static_cast<int>(num);
      return num;
    }
    case JSONMV::JSONType::json_str:
      return parser.getString(value);
    default:
      throw std::runtime_error("Unsupported JSON value type for input");
    }
  }

  // Convert array of JSON values to tuple of expected types
  template <typename... Ts>
  std::tuple<Ts...> parseArgs(const JSONMV::JSONArray &arr) const {
    if (arr.size() != sizeof...(Ts)) {
      throw std::runtime_error(
          "Argument count mismatch with solution signature");
    }
    return parseArgsImpl<Ts...>(arr, std::index_sequence_for<Ts...>{});
  }

  template <typename... Ts, std::size_t... Is>
  std::tuple<Ts...> parseArgsImpl(const JSONMV::JSONArray &arr,
                                  std::index_sequence<Is...>) const {
    return std::make_tuple(castTo<Ts>(parseJsonValue(arr[Is]))...);
  }

  template <typename X> X castTo(const std::any &val) const {
    if constexpr (std::is_same_v<X, int>) {
      return std::any_cast<int>(val);
    } else if constexpr (std::is_same_v<X, double>) {
      return std::any_cast<double>(val);
    } else if constexpr (std::is_same_v<X, bool>) {
      return std::any_cast<bool>(val);
    } else if constexpr (std::is_same_v<X, std::string>) {
      return std::any_cast<std::string>(val);
    } else {
      static_assert(sizeof(X) == 0, "Unsupported type for castTo");
    }
  }

  bool compareAny(const std::any &a, const std::any &b) const {
    if (a.type() != b.type()) {
      if ((a.type() == typeid(int) && b.type() == typeid(double)) ||
          (a.type() == typeid(double) && b.type() == typeid(int))) {
        return std::any_cast<double>(a) == std::any_cast<double>(b);
      }
      return false;
    }

    if (a.type() == typeid(bool)) {
      return std::any_cast<bool>(a) == std::any_cast<bool>(b);
    } else if (a.type() == typeid(int)) {
      return std::any_cast<int>(a) == std::any_cast<int>(b);
    } else if (a.type() == typeid(double)) {
      return std::any_cast<double>(a) == std::any_cast<double>(b);
    } else if (a.type() == typeid(std::string)) {
      return std::any_cast<std::string>(a) == std::any_cast<std::string>(b);
    }

    throw std::runtime_error("Unsupported type for comparison");
  }

  void printAny(const std::any &value) const {
    if (value.type() == typeid(bool)) {
      std::cout << std::boolalpha << std::any_cast<bool>(value);
    } else if (value.type() == typeid(int)) {
      std::cout << std::any_cast<int>(value);
    } else if (value.type() == typeid(double)) {
      std::cout << std::any_cast<double>(value);
    } else if (value.type() == typeid(std::string)) {
      std::cout << "\"" << std::any_cast<std::string>(value) << "\"";
    } else {
      std::cout << "Unsupported type";
    }
  }

  // Utility to print tuple
  template <typename Tuple, std::size_t... Is>
  void printTupleImpl(const Tuple &t, std::index_sequence<Is...>) const {
    ((printAny(std::get<Is>(t)),
      std::cout << (Is + 1 < sizeof...(Is) ? ", " : "")),
     ...);
  }

  template <typename... Ts> void printTuple(const std::tuple<Ts...> &t) const {
    printTupleImpl(t, std::index_sequence_for<Ts...>{});
  }
};

// Helper deduction machinery
template <typename T> struct MethodTraits;

// Specialization for pointer-to-member-function
template <typename C, typename R, typename... Args>
struct MethodTraits<R (C::*)(Args...)> {
  using ClassType = C;
  using ReturnType = R;
  using ArgTuple = std::tuple<Args...>;
};

template <typename C, typename R, typename... Args>
struct MethodTraits<R (C::*)(Args...) const> {
  using ClassType = C;
  using ReturnType = R;
  using ArgTuple = std::tuple<Args...>;
};

// Factory
template <typename T>
auto makeHelper(T &instance, const std::string &filename) {
  using Traits = MethodTraits<decltype(&T::solution)>;
  using R = typename Traits::ReturnType;
  using ArgTuple = typename Traits::ArgTuple;

  return std::apply(
      [&](auto &&...args) {
        return Helper<T, R, std::decay_t<decltype(args)>...>(filename);
      },
      ArgTuple{});
}

#endif
