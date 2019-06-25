
#include <vector>
#include <iostream>


int main() {
  std::vector<int> arr = {1,2,3,4};
  auto a = arr;
  arr.clear();
  for (auto v: a) {
    std::cout << v << '\n';
  }
  
  return 0;
}
