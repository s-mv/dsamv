#include <bits/stdc++.h>
using namespace std;

const int MAXN = 5e5 + 5;

int dist[MAXN], w[MAXN];
vector<int> adj[MAXN];
bool visited[MAXN];

void compute_dist(int n) {
  queue<int> q;
  fill(dist, dist + n + 1, -1);
  dist[1] = 0;
  q.push(1);
  while (!q.empty()) {
    int u = q.front();
    q.pop();
    for (int v : adj[u]) {
      if (dist[v] == -1) {
        dist[v] = dist[u] + 1;
        q.push(v);
      }
    }
  }
}

int simulate(int st, int n) {
  queue<tuple<int, int, int>> q;
  q.push({st, 1, 0});

  set<pair<int, int>> visited;

  int max_moves = 0;

  while (!q.empty()) {
    auto [u, life, time] = q.front();
    q.pop();

    life += w[u];
    if (life <= 0)
      continue;
    if (dist[u] <= time)
      continue;

    max_moves = max(max_moves, time);

    for (int v : adj[u]) {
      if (!visited.count({v, time + 1})) {
        visited.insert({v, time + 1});
        q.push({v, life, time + 1});
      }
    }
  }

  return max_moves;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);

  int T;
  cin >> T;
  while (T--) {
    int n, st;
    cin >> n >> st;

    for (int i = 1; i <= n; ++i) {
      cin >> w[i];
      adj[i].clear();
    }

    for (int i = 0; i < n - 1; ++i) {
      int u, v;
      cin >> u >> v;
      adj[u].push_back(v);
      adj[v].push_back(u);
    }

    compute_dist(n);
    cout << simulate(st, n) << "\n";
  }
  return 0;
}
