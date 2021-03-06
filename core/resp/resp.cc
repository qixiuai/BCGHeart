
#include "resp/resp.h"

#include <vector>

#include <iostream>

namespace bcg {
  namespace resp {
  
  Status Resp::push_back(float sample) {
    Status status = true;
    sample = lowpass_filter_.filter(sample);
    sample = energy_filter_.filter(sample);
    autopeak_.findpeaks(sample);
    return status;
  }
  
  std::vector<uint64_t> Resp::peak_indices() {
    auto peak_indices = autopeak_.peak_indices();
    for (auto index : peak_indices) {
      if (last_peak_index_ != 0) {
	peak_intervals_.push_back(index - last_peak_index_);
	last_peak_index_ = index;
      }
      else {
	peak_indices.erase(peak_indices.begin());
	last_peak_index_ = index;
      }
    }
    return peak_indices;
  }

  int Resp::num_peak_intervals() {
    return peak_intervals_.size();
  }

  std::vector<int> Resp::peak_intervals() {
    this->peak_indices();
    // TODO check whether it is deep copy
    auto intervals = peak_intervals_;
    peak_intervals_.clear();
    return intervals;
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
}




