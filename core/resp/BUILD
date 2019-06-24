
package(
    default_visibility = ["//visibility:public"],
)

licenses(["notice"])

cc_library(
    name = "resp",
    srcs = ["resp.cc"], 
    hdrs = ["resp.h"],
    data = ["//:data"],
    deps = ["//signal:filter", ":autopeaks"],
    copts = ["-std=c++17"],
)

cc_library(
    name  = "autopeaks",
    srcs  = ["autopeaks.cc"],
    hdrs  = ["autopeaks.h"],
    copts = ["-std=c++17"],
    deps = [":findpeaks_offline"],
)

cc_library(
    name  = "findpeaks_offline",
    srcs  = ["findpeaks.cc"],
    hdrs  = ["findpeaks.h"],
    copts = ["-std=c++17"],
    deps = ["//third_party/boost:boost"],
)
