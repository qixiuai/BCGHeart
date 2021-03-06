#ifndef SIGNAL_FILTER_
#define SIGNAL_FILTER_

#include <algorithm>
#include <vector>
#include <iostream>
#include <fstream>

#include "boost/circular_buffer.hpp"

namespace bcg {

namespace signal {
  template <class T>
  using Buffer = boost::circular_buffer<T>;

  class LinearFilter {
  public:
    LinearFilter() {}
    LinearFilter(std::string B_path, std::string A_path);
    LinearFilter(std::string B_path);
    LinearFilter(std::vector<double> B, std::vector<double> A);
    double filter(double value);
 
  private:
    std::vector<double> B;
    std::vector<double> A;
    Buffer<double> X;
    Buffer<double> Y;
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

  class EnergyFilter {
  public:
    EnergyFilter() {}
    EnergyFilter(int kernel_size) {
      kernel_size_ = kernel_size;
      signal_ = Buffer<float>(kernel_size);
    }
    float filter(float value);
  
  private:
    Buffer<float> signal_;
    int kernel_size_;
    float energy_ = 0;
  };

} // end namespace filter

}

#endif
