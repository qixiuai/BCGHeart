
#include "resp/resp.h"

#include <vector>

#include <iostream>

namespace bcg {

  
  Status Resp::push_back(float sample) {
    Status status = true;
    sample = lowpass_filter_.filter(sample);
    sample = energy_filter_.filter(sample);
    autopeak_.findpeaks(sample);
    return status;
  }
  
  std::vector<uint64_t> Resp::peak_indices() {
    return autopeak_.peak_indices();
  }

  /*
  std::vector<int> Resp::get_resp_intervals() const {
    std::vector<int> intervals;
    return intervals;
  }

  std::vector<int> Resp::get_resp_rates() const {
    std::vector<int> resp_rates;
    return resp_rates;
  } 
  */ 
}




