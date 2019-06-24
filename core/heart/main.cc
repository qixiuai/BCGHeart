
#include "findpeaks.h"

using namespace bcg::heart;

int main() {
  Buffer<float> signal={1,2,3};
  findpeaks_offline(signal, 12, 0.1, "up", 12);
  
  return 0;
}
