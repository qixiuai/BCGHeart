package(
    default_visibility = ["//visibility:public"],
)

licenses(["notice"])

cc_library(
    name = "heart",
    srcs = ["heart.cc"],
    hdrs = ["heart.h"],
    deps = [":autopeaks", "//signal:filter", "//monitor:monitor"],
)

cc_library(
    name = "autopeaks",
    srcs = ["autopeaks.cc"],
    hdrs = ["autopeaks.h"],
    deps = [":findpeaks_offline", "//signal:lib"],
)

cc_binary(
    name = "findpeaks_main",
    srcs = ["main.cc"],
    deps = ["findpeaks_offline"],
)

cc_library(
    name = "findpeaks_offline",
    srcs = ["findpeaks.cc"],
    hdrs = ["findpeaks.h"],
    deps = ["//third_party/boost:boost",
            "//signal:lib"],
)





