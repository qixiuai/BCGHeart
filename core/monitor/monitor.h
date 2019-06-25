
#ifndef MONITOR_MONITOR_H_
#define MONITOR_MONITOR_H_

#include <vector>
#include <cstdint>

namespace bcg {
  
  class Monitor {
  public:
    virtual bool push_back(float sample) = 0;
    virtual int num_peak_intervals() = 0;
    virtual std::vector<int> peak_intervals() = 0;
    virtual std::vector<uint64_t> peak_indices() = 0;
    virtual ~Monitor() = 0;
  };

}

#endif
