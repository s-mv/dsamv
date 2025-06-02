#include <iostream>
#include <string>
#include <unordered_map>

class Solution {
public:
  std::unordered_map<std::string, bool> tests = {
      {"you shall not pass", false},
      {"you can", true},
      {"you cannot", false},
      {"maybe no?", true},
  };

  bool solution(std::string input) {
    // Write the actual logic of the solution
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

int main() {
  Solution s;

  // Example test case execution
  for (std::pair<std::string, bool> test : s.tests) {
    std::cout << "Running input '" << test.first << "' -> "
              << (s.solution(test.first) == test.second ? "PASSED" : "FAILED")
              << std::endl;
  }
  return 0;
}
