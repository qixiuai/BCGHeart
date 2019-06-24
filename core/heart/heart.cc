
#include "heart/heart.h"

namespace bcg {
  namespace heart {

    Heart::Heart(int fs) {
      std::string data_dir = "/home/guo/BCGHeart/embedding/data/";
      std::string b_path = data_dir + "bcg_bandpass_1_15_b_" + std::to_string(fs) + ".csv";
      std::string a_path = data_dir + "bcg_bandpass_1_15_a_" + std::to_string(fs) + ".csv";
      signal::LinearFilter bandpass_filter(b_path, a_path);
      bandpass_filter_ = bandpass_filter;
      master_ = AutoPeaksMaster(fs);
    }
    
    bool Heart::push_back(float sample) {
      sample = bandpass_filter_.filter(sample);
      master_.findpeaks(sample);
      return true;
    }
    
    std::vector<uint64_t> Heart::peak_indices() {
      return master_.peak_indices();
    }
    
    std::vector<int> Heart::peak_intervals() {
      return master_.peak_intervals();
    }

    std::vector<int> Heart::num_peak_intervals() {
      return master_.num_peak_intervals();
    }
    
  }
}
