
#ifndef BCG_API_H_
#define BCG_API_H_

// init monitor
void* create_heart_monitor();
void* create_resp_monitor();

// push signal to monitor
void push_back(void* monitor, float sample);

// fetch intervals from monitor
int num_peak_intervals(void* monitor);
int peak_intervals(void* monitor, int* intervals);

// destroy monitor
void destroy_heart_monitor(void* monitor);
void destroy_resp_monitor(void* monitor);


#endif
