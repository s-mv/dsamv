#include <iostream>
#include <string>
#include <unordered_map>

#include "Helper.hpp"
#include "JSON.hpp"

/*
 * Hello C++ users.
 *
 * This cost me half a leg but I like to think it will save you some time.
 * Solution::solution is the function you need to implement.
 * The input and output values can be tweaked to anything.
 *
 * Cheers,
 * smv.
 */

class Solution {
public:
  float solution(int xoxox) { return 0.f; }
};

int main(int argc, char *argv[]) {
  try {
    Solution solution;
    auto tester = makeHelper(solution, argv[argc - 1]);
    tester.runTests(solution);
  } catch (const std::exception &ex) {
    std::cerr << "Error: " << ex.what() << std::endl;
    return 1;
  }
  return 0;
}
