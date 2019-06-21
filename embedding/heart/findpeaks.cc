
#include "heart/findpeaks.h"

#include <fstream>
#include <iostream>
#include <algorithm>
#include <cmath>
#include "signal/lib/lib.h"
#include <vector>
#include <string>

namespace bcg {
  namespace heart {

    bool operator> (const Peak& p1, const Peak& p2) {
      float peak_score = 0;
      if (p1.direction == "up")
	peak_score = p1.peak_value > p2.peak_value;
      else if (p1.direction == "down")
	peak_score = p1.peak_value < p2.peak_value;
      else
	throw;
      float l1_score = p1.front_value + p1.back_value > p2.front_value + p2.back_value;
      float l2_score = p1.front_front_value + p1.back_back_value > p2.front_front_value + p2.back_back_value;
      float score = peak_score + l1_score + l2_score;
      if (score >= 2)
	return true;
      return false;
    }

    std::vector<Peak>
    findpeaks_offline(const Buffer<float>& signal, float thres, int min_dist, 
		      std::string direction, int energy_window) {
      std::ofstream ofs("/home/guo/BCGHeart/embedding/test/debug.signal");
      for (auto value : signal) {
	ofs << std::to_string(value)+"\n";
      }
      
      //std::cerr << "entering findpeaks_offline\n";
      int num_samples = signal.size();
      std::vector<float> diff1_signal = signal::diff(signal);
      std::vector<float> diff1_abs_signal;
      diff1_abs_signal.resize(diff1_signal.size());
      std::transform(diff1_signal.begin(), diff1_signal.end(),
		     diff1_abs_signal.begin(),
		     [](float value){return std::abs(value);});
      //std::vector<float> diff2_signal = diff<std::vector<float>>(diff1_signal);
      float signal_max = *std::max_element(signal.begin(), signal.end());
      float signal_min = *std::min_element(signal.begin(), signal.end());
      float thres_signal =  0.5 * (signal_max - signal_min) + signal_min;
      //std::cerr << "thres_signal: " << thres_signal << '\n';
      std::vector<Extrema> maximas;
      int num_diff1_abs = diff1_abs_signal.size();
      for (int ind = 1; ind < num_diff1_abs; ind++) {
	float value = diff1_abs_signal[ind];
	if (diff1_abs_signal[ind] > diff1_abs_signal[ind-1] and
	    diff1_abs_signal[ind] > diff1_abs_signal[ind+1]) {
	  // TODO check value many 0s
	  maximas.push_back(Extrema(ind+1, value, "max"));
	}
      }
      
      std::vector<Extrema> minimas;
      if (direction == "up") {
	for (int ind = 1; ind < num_samples - 1; ind++) {
	  float value = signal[ind];
	  if (signal[ind] >= signal[ind-1] &&
	      signal[ind] >= signal[ind+1] &&
	      value > thres_signal) {
	    minimas.push_back(Extrema(ind, 0, "min"));
	  }
	}
      } else if (direction == "down") {
	for (int ind = 1; ind < num_samples - 1; ind++) {
	  float value = signal[ind];
	  if (signal[ind] <= signal[ind-1] &&
	      signal[ind] <= signal[ind+1] &&
	      value < thres_signal) {
	    minimas.push_back(Extrema(ind, 0, "min"));
	  }
	}
      } else {
	
      }

      std::sort(maximas.begin(), maximas.end(),
		[](const Extrema& lhs, const Extrema& rhs){
		  return lhs.value > rhs.value;
		});
      int num_maximas = maximas.size();
      maximas.resize(0.8*num_maximas);
      
      std::vector<Extrema> extremas;
      extremas.insert(extremas.end(), maximas.begin(), maximas.end());
      extremas.insert(extremas.end(), minimas.begin(), minimas.end());
      std::sort(extremas.begin(), extremas.end(),
		[](const Extrema& lhs, const Extrema& rhs){
		  return lhs.index < rhs.index;
		});
      //std::cerr << "extremas ready!\n";
      std::vector<Peak> j_peaks;
      
      if (extremas.size() < 5) {
	return j_peaks;
      }

      auto make_peak = [&](Extrema zero,
			  Extrema front, Extrema front_front,
			  Extrema back, Extrema back_back) {
	int peak_index = zero.index;
	float peak_value = signal[peak_index];
	int front_index = front.index;
	float front_value = diff1_abs_signal[front_index-1];
	int front_front_index = front_front.index;
	float front_front_value = front_front.value;
	int back_index = back.index;
	float back_value = back.value;
	int back_back_index = back_back.index;
	float back_back_value = back_back.value;
	float indicator_value = front_value + back_value;
	int window_st = peak_index - energy_window;
	if (window_st < 0) window_st = 0;
	int window_ed = peak_index + energy_window;
	if (window_ed > num_samples - 1)
	  window_ed = num_samples - 1;
	float peak_energy = 0;
	for (int ind = window_st; ind < window_ed; ind++) {
	  auto value = diff1_abs_signal[ind];
	  peak_energy += value * value;
	}
	float peak_score = 0;
	return Peak(peak_index, peak_value,
		    front_index, front_value,
		    front_front_index, front_front_value,
		    back_index, back_value,
		    back_back_index, back_back_value,
		    indicator_value, direction,
		    peak_energy, peak_score);
      };
      
      std::vector<Peak> raw_peaks;
      Extrema curr_extrema, prev_extrema, prev_prev_extrema, next_extrema, next_next_extrema;
      int num_extremas = extremas.size();
      for (int ind = 2; ind < num_extremas - 2; ind++) {
	curr_extrema = extremas[ind];
	if (curr_extrema.category != "min")
	  continue;
	auto prev_extrema_it = std::find_if(extremas.rend()-ind-1, extremas.rend(),
					    [](Extrema extrema){
					      return extrema.category == "max";
					    });
	if (prev_extrema_it != extremas.rend())
	  prev_extrema = *prev_extrema_it;
	else
	  continue;
	auto prev_prev_extrema_it = std::find_if(prev_extrema_it + 1, extremas.rend(),
						 [](Extrema extrema){
						   return extrema.category == "max";
						 });
	if (prev_prev_extrema_it != extremas.rend())
	  prev_prev_extrema = *prev_prev_extrema_it;
	else
	  continue;

	auto next_extrema_it = std::find_if(extremas.begin()+ind+1, extremas.end(),
					    [](Extrema extrema){
					      return extrema.category == "max";
					    });
	if (next_extrema_it != extremas.end())
	  next_extrema = *next_extrema_it;
	else
	  continue;
	
	auto next_next_extrema_it = std::find_if(next_extrema_it + 1, extremas.end(),
						 [](Extrema extrema){
						   return extrema.category == "max";
						 });
	if (next_next_extrema_it != extremas.end())
	  next_next_extrema = *next_next_extrema_it;
	else
	  continue;
	
	auto peak = make_peak(curr_extrema,
			      prev_extrema, prev_prev_extrema,
			      next_extrema, next_next_extrema);
	raw_peaks.push_back(peak);
      }
      if (raw_peaks.size() == 0)
	return j_peaks;
      //std::cerr << "raw peaks ready!\n";
      // add peak score
      for (auto& curr_peak : raw_peaks) {
	float score = 0;
	for (auto peak : raw_peaks) {
	  if (curr_peak > peak)
	    score += 1;
	}
	curr_peak.peak_score = score;
      }
      //std::cerr << "add peak score to raw peaks!\n";
      float max_indicator = std::max_element(raw_peaks.begin(), raw_peaks.end(),
					     [](Peak lp, Peak rp){
					       return lp.indicator_value > rp.indicator_value;
					     })->indicator_value;
      float min_indicator = std::min_element(raw_peaks.begin(), raw_peaks.end(),
					     [](Peak lp, Peak rp){
					       return lp.indicator_value < rp.indicator_value;
					     })->indicator_value;
      float thres_abs = min_indicator + thres * (max_indicator - min_indicator);
      //std::cerr << "cac thres_abs of indicator!\n";
      std::vector<Peak> peaks;
      std::copy_if(raw_peaks.begin(), raw_peaks.end(),
		   std::back_inserter(peaks),
		   [thres_abs](Peak p){
		     return p.indicator_value > thres_abs;
		   });
      if (peaks.size() == 0)
	return j_peaks;
      //std::cerr << "peaks ready!\n";
      std::vector<Peak> peaks_sorted(peaks.begin(), peaks.end());
      std::sort(peaks_sorted.begin(), peaks_sorted.end(), [](Peak lp, Peak rp){
	  return lp.peak_score > rp.peak_score;
	});
      //std::cerr << "peaks sorted!\n";
      auto masks = std::vector<bool>(num_samples, true);
      //std::cout << "masks size: " << masks.size() << '\n';
      for (const auto peak: peaks_sorted) {
        int peak_index = peak.peak_index;
	//std::cout << peak_index << '\n';
        if (masks[peak_index]) {
          auto sl_st = std::max(0, peak_index - min_dist);
          auto sl_ed = std::min(num_samples - 1, peak_index + min_dist);
          for (int ind = sl_st; ind <= sl_ed; ind++)
            masks[ind] = false;
          masks[peak_index] = true;
        }
      }
      //std::cerr << "masks end\n";
      for (const auto& peak : peaks) {
        int peak_index = peak.peak_index;
	//std::cerr << "peak index: " << peak_index << '\n';
        if (masks[peak_index])
          j_peaks.push_back(peak);
      }
      //std::cerr << "findpeaks offlines ended!\n";
      return j_peaks;
    }

  } 

}




