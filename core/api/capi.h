
#ifndef BCG_API_H_
#define BCG_API_H_

#include <stdint.h>
#include "monitor/monitor.h"
#include "heart/heart.h"
#include "resp/resp.h"

using bcg::Monitor;
using HeartMonitor = bcg::heart::Heart;
using RespMonitor = bcg::resp::Resp;

#ifdef __cplusplus
extern "C" {
#endif
  
  // init monitor
  HeartMonitor* create_heart_monitor();
  RespMonitor* create_resp_monitor();

  // push signal to monitor
  void push_back(Monitor* monitor, float sample);

  int num_peak_intervals(Monitor* monitor);
  int peak_intervals(Monitor* monitor, int* intervals);
  int peak_indices(Monitor* monitor, uint64_t* indices);
  
  // destroy monitor
  void destroy_monitor(Monitor* monitor);

#ifdef __cplusplus
}
#endif
  

#endif
