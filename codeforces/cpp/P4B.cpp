#include <iostream>
#include <vector>

int main() {
  int n, d;
  std::cin >> n >> d;

  std::vector<int> a(n), b(n), result(n);
  int min_total = 0, max_total = 0;

  for (int i = 0; i < n; ++i) {
    std::cin >> a[i] >> b[i];
    min_total += a[i];
    max_total += b[i];
    result[i] = a[i];
  }

  if (d < min_total || d > max_total) {
    std::cout << "NO\n";
    return 0;
  }

  int remaining = d - min_total;

  for (int i = 0; i < n && remaining > 0; ++i) {
    int extra = std::min(b[i] - a[i], remaining);
    result[i] += extra;
    remaining -= extra;
  }

  std::cout << "YES\n";
  for (int i = 0; i < n; ++i)
    std::cout << result[i] << " ";
  std::cout << "\n";

  return 0;
}
