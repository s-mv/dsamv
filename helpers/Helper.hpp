#ifndef TEST_HELPER_HPP
#define TEST_HELPER_HPP

#include "JSON.hpp"

#include <fstream>
#include <iostream>
#include <string>

template <typename T> class Helper {
public:
  Helper(const std::string &filename) {
    std::ifstream file(filename);
    if (!file) {
      throw std::runtime_error("Failed to open file: " + filename);
    }

    std::string jsonContent((std::istreambuf_iterator<char>(file)),
                            std::istreambuf_iterator<char>());

    root = parser.parse(jsonContent);
    testCases = parser.getObject(root);
  }

  void runTests(T &solutionInstance) const {
    int passed = 0, total = 0;

    for (const auto &pair : testCases) {
      const std::string &input = pair.first;
      bool expected = parser.getBool(pair.second);
      bool result = solutionInstance.solution(input);

      std::cout << "Input: \"" << input << "\" | Expected: " << std::boolalpha
                << expected << " | Got: " << result;

      if (result == expected) {
        std::cout << " PASSED\n";
        passed++;
      } else {
        std::cout << " FAILED\n";
      }

      total++;
    }

    std::cout << "\nPassed " << passed << " out of " << total
              << " test cases.\n";
  }

private:
  JSONMV parser;
  std::shared_ptr<JSONMV::JSONValue> root;
  JSONMV::JSONObject testCases;
};

#endif
