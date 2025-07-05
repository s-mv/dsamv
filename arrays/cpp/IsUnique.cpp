#include <iostream>
#include <string>
#include <unordered_map>

int main() {
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

  std::cout << (unique ? "true" : "false") << '\n';

  return 0;
}
