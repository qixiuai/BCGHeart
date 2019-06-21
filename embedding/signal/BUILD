
package(
    default_visibility = ["//visibility:public"],
)

licenses(["notice"])

cc_library(
    name = "lib",
    srcs = ["lib/lib.cc"],
    hdrs = ["lib/lib.h"],
)

cc_library(
    name = "histogram",
    srcs = ["histogram.cc"],
    hdrs = ["histogram.h"],
)

cc_test(
    name = "histogram_test",
    srcs = ["histogram_test.cc"],
)

cc_library(
    name = "filter",
    srcs = ["filter/filter.cc"],
    hdrs = ["filter/filter.h"],
    deps = ["//third_party/boost:boost"],
)

cc_binary(
    name = "filter_test",
    srcs = ["filter_test.cc"],
    deps = [":filter"],
)

cc_library(
    name = "resample",
    srcs = ["resample/resample.cc", "resample/upfirdn.h"],
    hdrs = ["resample/resample.h"],
    deps = ["//third_party/boost:boost"],
)

cc_binary(
    name = "resample_test",
    srcs = ["resample/resample_test.cc"],
    deps = [":resample"],
)




cc_binary(
    name  = "findpeaks_test",
    srcs  = ["findpeaks/findpeaks_test.cc"],
    deps = [":findpeaks"],
)
