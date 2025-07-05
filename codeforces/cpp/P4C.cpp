#include <iostream>
#include <unordered_map>

int main() {
  std::unordered_map<std::string, int> users;
  int n;
  std::cin >> n;

  for (int i = 0; i < n; ++i) {
    std::string name;
    std::cin >> name;

    if (users.find(name) == users.end()) {
      std::cout << "OK\n";
      users[name] = 1;
    } else {
      std::string newName = name + std::to_string(users[name]);
      std::cout << newName << "\n";
      users[name]++;
      users[newName] = 1;
    }
  }

  return 0;
}
