
#include "burn/lib/findpeaks/findpeaks.h"

namespace burn {
  namespace lib {

    std::vector<int> argsort(const std::vector<int>& vec) {
      std::vector<int> indexes = std::vector<int>(vec.size());
      std::iota(indexes.begin(), indexes.end(), 0);
      std::sort(indexes.begin(), indexes.end(),
		[&vec](std::size_t i1, std::size_t i2)
		{
		  return vec[i1] > vec[i2];
		});
      return indexes;
    }

    std::vector<int> argsort(const std::vector<double>& vec) {
      std::vector<int> indexes = std::vector<int>(vec.size());
      std::iota(indexes.begin(), indexes.end(), 0);
      std::sort(indexes.begin(), indexes.end(),
		[&vec](std::size_t i1, std::size_t i2)
		{
		  return vec[i1] > vec[i2];
		});
      return indexes;
    }


    int argmax(const std::vector<int>& hist) {
      int max_value = 0;
      int max_index = -1;
      for (unsigned int i=0; i < hist.size(); i++) {
	if (hist[i] > max_value) {
	  max_value = hist[i];
	  max_index = i;
	}
      }
      return max_index;
    }

    int get_median(std::vector<int> vec) {
      int vec_size = vec.size();
      if (vec_size == 1)
	return vec[0];
      std::sort(vec.begin(), vec.end());  
      auto div_ret = div(vec_size, 2);
      if (div_ret.rem == 0)
	return vec[vec_size/2];
      auto v1 = vec[vec_size/2];
      auto v2 = vec[vec_size/2-1];
      return (v1+v2)/ 2.0;
    }

    int get_most_common(const std::vector<int>& cycles, int num_bins) {
      assert(cycles.size() >= 1);
      if (cycles.size() == 1) {
	return cycles[0];
      }
      if (cycles.size() <= 5) {
	int m = 0;
	for (auto c: cycles) {
	  m += c;
	}
	return m / cycles.size();
      }
  
      int min = *std::min_element(cycles.begin(), cycles.end());
      int max = *std::max_element(cycles.begin(), cycles.end());
      float bin_len = (max - min) / float(num_bins-1);

      std::vector<int> histarr(num_bins, 0); // index -- count
      for (const auto cycle : cycles) {
	int bin_id = (cycle - min) / bin_len;
	histarr[bin_id] += 1;
      }
      int max_bin_id = argmax(histarr);

      std::vector<int> selected_cycles;
      float bin_lower = min + bin_len * max_bin_id;
      float bin_upper = min + bin_len * (max_bin_id + 1);
      for (auto cycle: cycles) {
	if (cycle >= bin_lower && cycle < bin_upper)
	  selected_cycles.push_back(cycle);
      }
      //  print_vector(selected_cycles, "selected_cycles");
      int avg_cycle = get_median(selected_cycles);
      //  std::cout << "avg_cycle:" << avg_cycle << std::endl;
      return avg_cycle;
    }

    PeakDetector::PeakDetector(float threshold, int min_dist) {
      threshold_ = threshold;
      min_dist_  = min_dist;
      Fz_ = 500;
      buffer_size_ = Fz_ * 3;
      threshold_ = threshold;
      min_dist_ = min_dist;
    }

    std::vector<int> PeakDetector::detect_signal(const std::vector<float>& ecg) {
      int signal_size = ecg.size();
      std::vector<int> ipks;
      ipks.reserve(ecg.size()/250);

      for (int i = 0; i < signal_size; i += Fz_) {
	// parallel
	auto st = ecg.begin() + i;
	auto step = Fz_ * 3;
	auto ed = (i < signal_size - step) ? (ecg.begin() + i + step) : ecg.end();
	std::vector<float> signal_temp(st, ed);
	std::vector<int> ipks_temp = findpeaks<std::vector<float>>(signal_temp,
								   threshold_,
								   min_dist_);
	int ipk_max = Fz_ * 2;
	int ipk_min = Fz_; // to remove duplicate ipks
	for (int ind = 0; ind < static_cast<int>(ipks_temp.size()); ind++) {
	  auto ipk = ipks_temp[ind];
	  if (ipk <= ipk_min) continue;
	  if (ipk > ipk_max) break; // miss peaks at the signal end
	  ipks.push_back(ipk + i);
	}
      }

      return ipks;  
    }
    
  }
}
