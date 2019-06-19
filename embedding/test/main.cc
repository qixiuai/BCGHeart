
#include <stdexcept>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include "resp/resp.h"

using Status = bool;

Status load_bcg(std::vector<float>& signal, std::string filepath) {
  bool flag = true;
  std::ifstream in(filepath);
  if (!in.is_open()) {
    throw std::invalid_argument(filepath + " is not good!");
  }
  std::string line;
  while (std::getline(in, line)) {
    float value = std::stof(line);
    signal.push_back(value);
  }
  return flag;
}

std::vector<uint64_t> run_resp(const std::vector<float>& signal) {
  bcg::Resp resp(500);
  int num_samples = signal.size();
  std::vector<uint64_t> peak_indices;
  for (int ind = 0; ind < num_samples; ind++) {
    float sample = signal[ind];
    resp.push_back(sample);
    if (ind % 1000 == 0) {
      auto peak_indices_tmp = resp.fetch_peak_indices();
      for (auto peak_index : peak_indices_tmp) {
	peak_indices.push_back(peak_index);
      }
    }
  }
  return peak_indices;
}


int main() {
  std::vector<float> bcg;
  std::string data_dir = "/home/guo/BCGHeart/embedding/test/";
  std::string filename ="raw_bcg.txt";
  Status status = load_bcg(bcg, data_dir+filename);
  if (!status) {
    std::cerr << "something wrong with load_bcg\n";
  }
  //  std::cout << bcg.size() << '\n';
  auto indices = run_resp(bcg);
  for (auto index : indices) {
    std::cout << index << '\n';
  }
  
  return 0;
}

