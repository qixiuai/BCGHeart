
#ifndef HEART_AUTOPEAKS_H_
#define HEART_AUTOPEAKS_H_

#include <string>
#include <vector>
#include "heart/findpeaks.h"

namespace bcg {

namespace heart {


  class AutoPeaks {
  public:
    AutoPeaks() = default;
    AutoPeaks(float threshold, int min_dist,
	      std::string direction,
	      int energy_window, int buffer_size) {
      this->threshold_ = threshold;
      this->min_dist_ = min_dist;
      this->direction_ = direction;
      this->energy_window_ = energy_window;
      this->signal_ = Buffer<float>(buffer_size);
    }
    
    bool findpeaks(float sample);
    
    std::vector<uint64_t> peak_indices();
    
    bool reset();
    
  private:
    float threshold_;
    int min_dist_;
    std::string direction_;
    int energy_window_;
    
    Buffer<float> signal_;
    std::vector<uint64_t> peak_indices_;
    uint64_t signal_index_ = 0;
    int update_counter_ = 0;
  };  

  class AutoPeaksWorker {
  public:
    AutoPeaksWorker(AutoPeaks instance, int nsamples=60) {
      instance_ = instance;
      peak_indices_for_loss_ = Buffer<float>(nsamples);
    }
    bool findpeaks(float sample);
    std::vector<uint64_t> peak_indices();
    std::vector<int> peak_intervals();
    float loss();
    
  private:
    AutoPeaks instance_;
    Buffer<float> peak_indices_for_loss_;
    std::vector<uint64_t> peak_indices_;
    std::vector<int> peak_intervals_;
    uint64_t last_peak_index_ = 0;
  };

  
  class AutoPeaksMaster {
  public:
    AutoPeaksMaster() = default;
    AutoPeaksMaster(int fs) {
      counter_ = 0;
      counter_maximum_ = fs;
      std::vector<float> threses = {0.1, 0.2};
      //std::vector<float> threses = {0.2};
      std::vector<int> min_dists = {int(0.5*fs), int(0.6*fs), int(0.75*fs), int(0.85*fs)};
      //std::vector<int> min_dists = {int(0.6*fs)};
      std::vector<std::string> directions = {"up", "down"};
      //std::vector<std::string> directions = {"down"};
      std::vector<int> buffer_sizes = {4*fs};
      for (auto thres : threses) {
	for (auto min_dist : min_dists) {
	  for (auto direction : directions) {
	    for (auto buffer_size : buffer_sizes) {
	      int energy_window=int(0.15*fs);
	      auto findpeaks = AutoPeaks(thres,
					 min_dist,
					 direction,
					 energy_window,
					 buffer_size);
	      int nsamples = 6;
	      auto worker = AutoPeaksWorker(findpeaks, nsamples);
	      workers_.push_back(worker);
	    }
	  }
	}
      }
    }
    bool findpeaks(float sample);
    std::vector<int> peak_intervals();
    std::vector<uint64_t> peak_indices();

  private:
    std::vector<AutoPeaksWorker> workers_;
    std::vector<int> peak_intervals_;
    std::vector<uint64_t> peak_indices_;
    int counter_ = 0;
    int counter_maximum_ = 0;
  };



} // endspace autopeaks

}

#endif
