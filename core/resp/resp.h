
#ifndef BCG_RESP_H_
#define BCG_RESP_H_

#include <vector>
#include "signal/filter/filter.h"
#include "resp/autopeaks.h"

namespace bcg {

  using Status = bool;

  class Resp {
  private:
    signal::LinearFilter lowpass_filter_;
    //signal::MedianFilter median_filter_;
    signal::EnergyFilter energy_filter_;
    //autopeak_(thres=0.65, min_dist=2*fs, buffer_size=15*fs)
    autopeaks::AutoPeak autopeak_;
    int fs_ = 500;

  public:
    Resp() {}
    Resp(int fs) :
      energy_filter_(fs*1.5) {
      //std::string b_path = "filter/lowpass0.4_b_" + std::to_string(fs) + ".csv";
      std::string data_dir = "/home/guo/BCGHeart/embedding/data/";
      std::string b_path = data_dir + "lowpass0.4_b_" + std::to_string(fs) + ".csv";
      std::string a_path = data_dir + "lowpass0.4_a_" + std::to_string(fs) + ".csv";
      signal::LinearFilter lowpass_filter(b_path, a_path);
      lowpass_filter_ = lowpass_filter;
      float thres = 0.65;
      int min_dist = 2*fs;
      int buffer_size = 15*fs;
      autopeak_ = autopeaks::AutoPeak(thres, min_dist, buffer_size);
    }

    Status push_back(float sample);
    
    ~Resp() {}

    std::vector<uint64_t> peak_indices();
    //std::vector<int> get_resp_peak_intervals() const;
    //std::vector<int> get_resp_peak_rates() const;
  };

}


#endif