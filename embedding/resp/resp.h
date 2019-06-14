
#ifndef BCG_RESP_H_
#define BCG_RESP_H_

#include <vector>

namespace bcg {

  class Resp {
  private:
    // common-filter --> lowpass/median/custom transform filters
    LowpassFilter lowpass_filter_;
    MedianFilter median_filter_;
    AutoPeaks autopeaks_;
    
    Buffer<float> signal_;
    std::vector<int> intervals_;
    
  public:
    Resp();
    Resp(int fs);
  };

}


#endif
