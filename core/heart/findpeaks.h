
#ifndef HEART_FINDPEAKS_H_
#define HEART_FINDPEAKS_H_

#include <algorithm>
#include <string>
#include <vector>

#include "boost/circular_buffer.hpp"

namespace bcg {
  namespace heart {
  
    template <typename T>
    using Buffer = boost::circular_buffer<T>;
  
    struct Peak {
      int peak_index;
      float peak_value;
      int front_index;
      float front_value;
      int front_front_index;
      float front_front_value;
      int back_index;
      float back_value;
      int back_back_index;
      float back_back_value;
      float indicator_value;
      std::string direction;
      float peak_energy;
      float peak_score;
      Peak() = default;
      Peak(int peak_index, float peak_value,
	   int front_index, float front_value,
	   int front_front_index, float front_front_value,
	   int back_index, float back_value,
	   int back_back_index, float back_back_value,
	   float indicator_value, std::string direction,
	   float peak_energy, float peak_score) {
	this->peak_index = peak_index;
	this->peak_value = peak_value;
	this->front_index = front_index;
	this->front_value = front_value;
	this->front_front_index = front_front_index;
	this->front_front_value = front_front_value;
	this->back_index = back_index;
	this->back_value = back_value;
	this->back_back_index = back_back_index;
	this->back_back_value = back_back_value;
	this->indicator_value = indicator_value;
	this->direction = direction;
	this->peak_energy = peak_energy;
	this->peak_score = peak_score;
      }
      
      friend bool operator> (const Peak& p1, const Peak& p2);
    };

    struct Extrema {
      int index;
      float value;
      std::string category;
      Extrema() = default;
      Extrema(int index, float value, std::string category) {
	this->index = index;
	this->value = value;
	this->category = category;
      }
    };
  
    //int min_dist=300, float thres=0.7, std::string direction="up", int energy_window=75
    std::vector<Peak>
    findpeaks_offline(const Buffer<float>& signal, float thres, int min_dist, 
		      std::string direction, int energy_window);

  } // end namespace heart
} // end namespace bcg



#endif




