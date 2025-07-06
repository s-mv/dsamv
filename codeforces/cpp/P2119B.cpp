#include <cmath>
#include <iostream>
#include <vector>

bool possible(int a, int b, int x, int y, const std::vector<int> &dist) {
  long long dx = x - a;
  long long dy = y - b;
  long long required = dx * dx + dy * dy;
  const double EPS = 1e-5;

  long long total = 0;
  for (int d : dist)
    total += d;

  if (required == 0 && dist.size() == 0)
    return true;

  if (required == 0 && dist.size() == 1)
    return dist.at(0) <= 0;

  if (required == 0 && dist.size() == 2)
    return std::abs(dist.at(1) - dist.at(0)) <= 0 ||
           std::abs(dist.at(1) + dist.at(0)) <= 0;

  for (int d : dist)
    total += d;

  total *= total;

  long long rem = total - required;

  if (rem >= EPS)
    return true;

  return false;
}

int main() {
  int t;
  std::cin >> t;

  while (t--) {
    int n;
    std::cin >> n;
    int px, py, qx, qy;
    std::cin >> px >> py >> qx >> qy;

    std::vector<int> a(n);
    for (int i = 0; i < n; ++i) {
      std::cin >> a[i];
    }

    if (possible(px, py, qx, qy, a))
      std::cout << "Yes\n";
    else
      std::cout << "No\n";
  }

  return 0;
}
