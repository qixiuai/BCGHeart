
#include "signal/filter/filter.h"

#include <fstream>
#include <vector>

namespace signal {

static std::vector<float> load_csv(std::string path) {
    std::fstream in(path);
    if (!in.is_open()) {
      std::cout << path << " not found!" << std::endl;
      exit(0);
    }
    std::vector<float> coeff;
    std::string line;
    while (getline(in, line)) {
      std::string val_str = "";    
      while (line.length() > 0) {
	if (line[0] == ',') {
	  coeff.push_back(std::stof(val_str));
	  val_str = "";
	} else {
	  val_str += line[0];
	}
	line = line.substr(1);
      }
      if (val_str.length() > 0) {
	coeff.push_back(std::stof(val_str));
      }
    }
    return coeff;
  }
    
  LinearFilter::LinearFilter(std::vector<float> B, std::vector<float> A){
    this->B = B;
    this->A = A;
    this->X = Buffer<float>(B.size());
    this->Y = Buffer<float>(A.size());
  }

  LinearFilter::LinearFilter(std::string B_path, std::string A_path) {
    auto B = load_csv(B_path);
    auto A = load_csv(A_path);
    this->B = B;
    this->A = A;
    this->X = Buffer<float>(B.size());
    this->Y = Buffer<float>(A.size()-1);
  }

  LinearFilter::LinearFilter(std::string B_path) {
    auto B = load_csv(B_path);
    this->B = B;
    this->A = {1};
    this->X = Buffer<float>(B.size());
    this->Y = Buffer<float>(A.size()-1);
  }
    
  float LinearFilter::filter(float value) {
    this->X.push_back(value);
    float upper, lower;
    upper = lower = 0;
    int nb  = this->B.size();
    int na  = this->A.size();
    int nx  = this->X.size()-1;
    int ny  = this->Y.size();
    for (int i=0; nx-i>=0 && i<nb; i++) {
      upper += this->B[i]*this->X[nx-i];
    }
    for (int i=1; ny-i>=0 && i<na; i++) {
      lower += this->A[i]*this->Y[ny-i];
    }
    float y = upper - lower;
    this->Y.push_back(y);
    return y;
  }

  float MedianFilter::filter(float value) {
    this->X.push_back(value);
    if (this->X.size() <= 1)
      return value;
    std::vector<float> vec;
    vec.reserve(this->X.size());
    for (auto x : this->X)
      vec.push_back(x);
    int vec_size = vec.size();
    std::sort(vec.begin(), vec.end());
    return vec[vec_size/2];
  }

}
