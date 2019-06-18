
#include "resp/resp.h"

#include <vector>


namespace bcg {

  
  Status Resp::push_back(float sample) {
    Status status = true;
    sample = median_filter_.filter(sample);
    sample = lowpass_filter_.filter(sample);
    sample = energy_filter_.filter(sample);
    autopeaks_.findpeaks(sample);
    return status;
  }
  
  std::vector<int> Resp::get_resp_peak_indices() const {
    return autopeaks_.get_peak_indices();
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




