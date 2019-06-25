
#include "heart/heart.h"

namespace bcg {
  namespace heart {

    Heart::Heart(int fs) {
      //std::string data_dir = "/home/guo/BCGHeart/embedding/data/";
      //std::string b_path = data_dir + "bcg_bandpass_1_15_b_" + std::to_string(fs) + ".csv";
      //std::string a_path = data_dir + "bcg_bandpass_1_15_a_" + std::to_string(fs) + ".csv";
      std::vector<double> B = {0.01926379938884432985179984143542242236435413360595703125,
			       0,
			       -0.0385275987776886597035996828708448447287082672119140625,
			       0,
			       0.01926379938884432985179984143542242236435413360595703125};
      std::vector<double> A = {1,
			       -3.5665594108431211139986771740950644016265869140625,
			       4.781813278714054149531875737011432647705078125,
			       -2.863103128691474097422542399726808071136474609375,
			       0.6478537971948588047865769112831912934780120849609375};
      signal::LinearFilter bandpass_filter(B, A);
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

    int Heart::num_peak_intervals() {
      return master_.num_peak_intervals();
    }
    
  }
}
