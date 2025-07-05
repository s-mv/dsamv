#include <iostream>
#include <string>
#include <unordered_map>

int main() {
  // this code is equivalent to arrays/cpp/IsUnique.cpp
  // read input given by the runner
  std::string text;
  std::getline(std::cin, text);

  std::unordered_map<char, int> charCount;
  bool unique = true;
  for (char c : text) {
    if (++charCount[c] > 1) {
      unique = false;
      break;
    }
  }

  // print the output - this will be read by the tests
  std::cout << (unique ? "true" : "false") << '\n';

  return 0;
}
