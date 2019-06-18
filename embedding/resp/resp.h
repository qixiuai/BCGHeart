
#ifndef BCG_RESP_H_
#define BCG_RESP_H_

#include <vector>
#include "signal/filter/filter.h"
#include "resp/findpeaks.h"

namespace bcg {

  using Status = bool;
  
  class Resp {
  private:
    LowpassFilter lowpass_filter_;
    MedianFilter median_filter_;
    EnergyFilter energy_filter_;
    
    AutoPeaks autopeaks_;
    int fs_ = 500;

  public:
    Resp() {}
    Resp(int fs) {
      lowpass_filter_ = new LowpassFilter();
      median_filter_ = new MedianFilter();
      energy_filter_ = new EnergyFilter();
    }

    Status push_back(float sample);
    
    ~Resp() {
      delete lowpass_filter_;
      delete median_filter_;
      delete energy_filter_;
    }

    std::vector<int> get_resp_peak_indices() const;
    //std::vector<int> get_resp_peak_intervals() const;
    //std::vector<int> get_resp_peak_rates() const;
  };

}


#endif
