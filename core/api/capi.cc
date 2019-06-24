
#include "api/capi.h"

#include "heart/heart.h"
#include "resp/resp.h"

#ifdef __cplusplus__
extern "C" {
#endif

  // init monitor
  void* create_heart_monitor(int fs) {
    return new bcg::Heart(fs);
  }

  void* create_resp_monitor(int fs) {
    return new bcg::Resp(fs);
  }

  // push signal to monitor
  void push_back(void* monitor, float sample) {
    monitor->push_back(sample);
  }

  // fetch intervals from monitor
  int num_peak_intervals(void* monitor) {
    return monitor->num_peak_intervals();
  }

  int peak_intervals(void* monitor, int* dest) {
    auto intervals = monitor->peak_intervals();
    int num_intervals = intervals.size();
    for (int ind = 0; ind < num_intervals; ind++)
      dest[ind] = intervals[ind];
    return num_intervals;
  }

  // destroy monitor
  void destroy_monitor(void* monitor) {
    delete monitor;
  }

#ifdef __cplusplus__
}
#endif


