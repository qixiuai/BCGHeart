#ifndef _PSG_FINDPEAKS_
#define _PSG_FINDPEAKS_

#include <algorithm>
#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <numeric>
#include <memory>
#include <cstdlib>

#include "boost/circular_buffer.hpp"

namespace burn {
  namespace lib {

    using uint = unsigned int;

    template <typename T>
    using Buffer = boost::circular_buffer<T>;
    
    class PeakDetector {
    public:
      PeakDetector() = default;
      PeakDetector(float threshold, int min_dist);

      std::vector<int> detect_signal(const std::vector<float>& ecg);

    private:
      int Fz_ = 500;
      int buffer_size_ = Fz_ * 3;
      float threshold_ = 0.75;
      int min_dist_ = 115;
    };

    /*
    void print_vector(const std::vector<int>& vec, std::string info) {
      std::cout<< "\n"<<info<<":\n";
      for (auto v: vec) {
	std::cout << v << ',';
      }
      std::cout << '\n';
    }

    void print_buffer(const Buffer<int>& vec, std::string info) {
      std::cout<< "\n"<<info<<":\n";
      for (auto v: vec) {
	std::cout << v << ',';
      }
      std::cout << '\n';
    }
    */
    
    template <class T>
    std::vector<int> np_diff(const T& ipks) {
      std::vector<int> rets(ipks.size()-1);
      for (uint i=0; i<ipks.size()-1; i++) {
	rets[i] = ipks[i+1] - ipks[i];
      }
      return rets;
    }

    template <class T>
    std::vector<int> np_abs_diff(const T& ipks) {
      auto diffs = np_diff(ipks);
      std::vector<int> abs_diffs;
      abs_diffs.reserve(diffs.size());
      std::transform(diffs.begin(), diffs.end(), std::back_inserter(abs_diffs),
		     [](int diff) -> int { return std::abs(diff); } );
      return abs_diffs; 
    }

    std::vector<int> argsort(const std::vector<int>& vec);

    std::vector<int> argsort(const std::vector<double>& vec);

    template <class T>
    std::vector<int> get_highest_peaks(const T& signal, const std::vector<int>& ipks) {
      int num_peaks = ipks.size();
      std::vector<double> peak_values = std::vector<double>(num_peaks);
      for (int i=0; i < num_peaks; i++) {
	peak_values[i] = signal[ipks[i]];
      }
      auto indexes = argsort(peak_values);
      std::vector<int> highest = std::vector<int>(num_peaks);
      for (int i=0; i < num_peaks; i++) {
	highest[i] = ipks[indexes[i]];
      }
      return highest;
    }

    template <class T>
    std::vector<int> findpeaks(const T& signal, float threshold, int min_dist) {
      int len = signal.size();
      double signal_max = *std::max_element(signal.begin(), signal.end());
      double signal_min = *std::min_element(signal.begin(), signal.end());
      float thres = threshold * (signal_max - signal_min) + signal_min;
      std::vector<double> diffs(len-1);
      for (int i = 0; i<len-1; i++) {
	diffs[i] = signal[i+1] - signal[i];
      }
      std::vector<int> ipks;
      for (uint i = 0; i < diffs.size(); i++) {
	if (diffs[i]   >= 0 &&
	    diffs[i+1] <= 0 &&
	    signal[i] > thres) {
	  ipks.push_back(i+1);
	}
      }
      if (ipks.size() <= 1 || min_dist <= 1) {
	return ipks;
      }

      auto highest_ipks = get_highest_peaks<T>(signal, ipks);
      auto flags = std::vector<bool>(signal.size(), false);
      for (const auto idx: ipks)
	flags[idx] = true;

      for (const auto ipk: highest_ipks) {
	if (flags[ipk]) {
	  auto sl_st = std::max(0, ipk - min_dist);
	  auto sl_ed = std::min(int(signal.size()-1), ipk + min_dist);
	  for (int i=sl_st; i<=sl_ed; i++)
	    flags[i] = false;
	  flags[ipk] = true;
	}
      }  
      std::vector<int> ipks_selected;
      ipks_selected.reserve(128);
      for (uint i=0; i < flags.size(); i++) {
	if (flags[i]) {
	  ipks_selected.push_back(i);
	}
      }
      return ipks_selected;
    }

    int argmax(const std::vector<int>& hist);

    int get_median(std::vector<int> vec);

    int get_most_common(const std::vector<int>& cycles, int num_bins=10);

  } //end namespace lib

} //end namespace burn

#endif
