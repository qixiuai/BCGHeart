#ifndef SIGNAL_FILTER_
#define SIGNAL_FILTER_

#include <algorithm>
#include <vector>
#include <iostream>
#include <fstream>

#include "boost/circular_buffer.hpp"


namespace signal {
  template <class T>
  using Buffer = boost::circular_buffer<T>;
    
  class LinearFilter {
  public:
    LinearFilter() {}
    LinearFilter(std::string B_path, std::string A_path);
    LinearFilter(std::string B_path);
    LinearFilter(std::vector<float> B, std::vector<float> A);
    float filter(float value);
 
  private:
    std::vector<float> B;
    std::vector<float> A;
    Buffer<float> X;
    Buffer<float> Y;
  };

  class MedianFilter {
  public:
    MedianFilter() {}
    MedianFilter(int kernel_size){
      this->kernel_size = kernel_size;
      this->X = Buffer<float>(kernel_size);
    }
    float filter(float value);
  
  private:
    Buffer<float> X;
    int kernel_size;
  };



} // end namespace filter

#endif
