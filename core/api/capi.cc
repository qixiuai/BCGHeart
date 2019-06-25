
#include "api/capi.h"




// init monitor
HeartMonitor* create_heart_monitor(int fs) {
  return new bcg::heart::Heart(fs);
}

RespMonitor* create_resp_monitor(int fs) {
  return new bcg::resp::Resp(fs);
}

// push signal to monitor
void push_back(Monitor* monitor, float sample) {
  monitor->push_back(sample);
}

// fetch intervals from monitor
int num_peak_intervals(Monitor* monitor) {
  return monitor->num_peak_intervals();
}

int peak_intervals(Monitor* monitor, int* dest) {
  auto intervals = monitor->peak_intervals();
  int num_intervals = intervals.size();
  for (int ind = 0; ind < num_intervals; ind++)
    dest[ind] = intervals[ind];
  return num_intervals;
}

int peak_indices(Monitor* monitor, uint64_t* dest) {
  auto indices = monitor->peak_indices();
  int num_indices = indices.size();
  for (int ind = 0; ind < num_indices; ind++)
    dest[ind] = indices[ind];
  return num_indices;
}

// destroy monitor
void destroy_monitor(Monitor* monitor) {
  delete monitor;
}



