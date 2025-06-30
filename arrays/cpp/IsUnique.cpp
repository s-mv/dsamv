#include <iostream>
#include <string>
#include <unordered_map>

#include "Helper.hpp"
#include "JSON.hpp"

class Solution {
public:
  bool solution(std::string input) {
    std::unordered_map<char, int> charCount;
    for (char c : input) {
      charCount[c]++;
      if (charCount[c] > 1) {
        return false;
      }
    }
    return true;
  }
};

int main(int argc, char *argv[]) {
  try {
    Solution solution;
    Helper<Solution> tester(argv[argc - 1]);
    tester.runTests(solution);
  } catch (const std::exception &ex) {
    std::cerr << "Error: " << ex.what() << std::endl;
    return 1;
  }
  return 0;
}
