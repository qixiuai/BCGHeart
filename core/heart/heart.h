
#ifndef HEART_HEART_H_
#define HEART_HEART_H_

#include <vector>
#include <cstdint>

#include "monitor/monitor.h"
#include "signal/filter/filter.h"
#include "heart/autopeaks.h"


namespace bcg {
  namespace heart {

    class Heart : Monitor {
    public:
      Heart() = default;
      Heart(int fs=500);
      bool push_back(float sample) override;
      std::vector<uint64_t> peak_indices() override;
      std::vector<int> peak_intervals() override;
      int num_peak_intervals() override;
      ~Heart() override = default ;
      
    private:
      signal::LinearFilter bandpass_filter_;
      AutoPeaksMaster master_;
    };

    
  }
}


#endif

