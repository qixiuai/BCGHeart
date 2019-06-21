
#include <stdexcept>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include "heart/heart.h"
#include "resp/resp.h"
#include "signal/filter/filter.h"

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

void run_filter(const std::vector<float>& signal) {
  std::string data_dir = "/home/guo/BCGHeart/embedding/data/";
  int fs = 500;
  std::string b_path = data_dir + "bcg_bandpass_1_15_b_" + std::to_string(fs) + ".csv";
  std::string a_path = data_dir + "bcg_bandpass_1_15_a_" + std::to_string(fs) + ".csv";
  bcg::signal::LinearFilter bandpass_filter(b_path, a_path);
  int num_samples = signal.size();
  std::vector<uint64_t> peak_indices;
  for (int ind = 0; ind < num_samples; ind++) {
    float sample = signal[ind];
    auto new_sample = bandpass_filter.filter(sample);
    std::cout << new_sample << '\n';
  }
}


std::vector<uint64_t> run_resp(const std::vector<float>& signal) {
  bcg::Resp resp(500);
  int num_samples = signal.size();
  std::vector<uint64_t> peak_indices;
  for (int ind = 0; ind < num_samples; ind++) {
    float sample = signal[ind];
    resp.push_back(sample);
    if (ind % 1000 == 0) {
      auto peak_indices_tmp = resp.peak_indices();
      for (auto peak_index : peak_indices_tmp) {
	peak_indices.push_back(peak_index);
      }
    }
  }
  return peak_indices;
}


void run_heart(const std::vector<float>& signal) {
  bcg::heart::Heart heart(500);
  int num_samples = signal.size();
  std::vector<uint64_t> peak_indices;
  std::vector<uint64_t> peak_intervals;
  for (int ind = 0; ind < num_samples; ind++) {
    float sample = signal[ind];
    heart.push_back(sample);
    if (ind % 1000 == 0) {
      auto peak_indices_tmp = heart.peak_indices();
      for (auto peak_index : peak_indices_tmp) {
	peak_indices.push_back(peak_index);
      }
      auto intervals = heart.peak_intervals();
      for (auto interval : intervals) {
	peak_intervals.push_back(interval);
      }
    }
  }
  for (auto interval : peak_intervals) {
    std::cout << interval << '\n';
  }
}

int main() {
  std::vector<float> bcg;
  std::string data_dir = "/home/guo/BCGHeart/embedding/test/";
  //std::string filename ="raw_bcg.txt";
  std::string filename ="yjj_raw_bcg.txt";
  Status status = load_bcg(bcg, data_dir+filename);
  if (!status) {
    std::cerr << "something wrong with load_bcg\n";
  }
  //  std::cout << bcg.size() << '\n';
  //auto indices = run_resp(bcg);
  //  run_filter(bcg);
  
  run_heart(bcg);

  return 0;
}

