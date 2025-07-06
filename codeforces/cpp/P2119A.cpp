#include <iostream>

int problem(int a, int b, int x, int y) {
  if (a > b) {
    if (b == (a xor 1))
      return y;

    return -1;
  }

  if (a == b)
    return 0;

  int axor1 = a xor 1;

  if (a + 1 == axor1 && a + 1 == b) {
    return std::min(x, y);
  }

  if (a + 1 == b)
    return x;

  if (axor1 == b)
    return y;

  int cost = 0;

  while (a != b) {
    int aplus1 = a + 1;
    int axor1 = a xor 1;

    if (aplus1 == axor1) {
      cost += std::min(x, y);
      a++;
    }

    if (aplus1 > axor1) {
      cost += x;
      a++;
    }

    if (aplus1 < axor1) {
      if (a > axor1)
        return -1;
      cost += y;
      a = axor1;
    }
  }

  return cost;
}

/*
 */

int main() {
  int n;

  std::cin >> n;

  for (int i = 0; i < n; i++) {
    int a, b, x, y;
    std::cin >> a >> b >> x >> y;
    std::cout << problem(a, b, x, y) << "\n";
  }

  return 0;
}
