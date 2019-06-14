
#include <string>
#include <vector>
#include "findpeaks.h"

namespace autopeaks {

  class AutoPeaksMaster {
    
  };

  class AutoPeaksWorker {
    
  };

  template <class T>
  using Buffer = std::vector<T>;
  
  class AutoPeaks {
  public:
    AutoPeaks();
    
    int fs;
    Buffer<float> signal_buffer_;
    Buffer<float> peak_value_buffer_;
    Buffer<int> peak_index_buffer_;
    Buffer<findpeaks::Peak> peaks_buffer_;
    int signal_index_ = -1;
    int update_counter_ = 0;
    float thres;
    int min_dist;
    std::string direction;

    void peaks();
    void peak_values();
    void peak_indices();
 
    void findpeaks(float value) {
      signal_index_ += 1;
      update_counter_ += 1;
      signal_buffer_.push_back(value);
      if (!signal_buffer_.full())
	return;
      update_thres = signal_buffer_.capacity / 2;
      if (update_counter_ < update_thres)
	return;
      peaks = findpeaks::findpeaks(signal_buffer_, thres, min_dist, direction);
      
      
    }
    
    void clear();
  };

} // endspace autopeaks
