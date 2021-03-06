#!/usr/bin/env bash

CM4_COPTS="--copt=-march=armv7-m --copt=-mfpu=vfp
  --copt=-isystem
  --copt=-std=gnu11"

bazel build -c opt ${CM4_COPTS} \
  --cpu=armeabi-v7m \
  --crosstool_top=@local_config_arm_compiler//:toolchain \
  --verbose_failures \
  //demo:demo

#  --copt=-funsafe-math-optimizations \

