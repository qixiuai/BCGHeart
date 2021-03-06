# *-* python *-*

# Bazel rules for building swig files.
def _py_wrap_cc_impl(ctx):
    srcs = ctx.files.srcs
    if len(srcs) != 1:
        fail("Exactly one SWIG source file label must be specified.", "srcs")
    module_name = ctx.attr.module_name
    src = ctx.files.srcs[0]
    inputs = _get_transitive_headers([src] + ctx.files.swig_includes, ctx.attr.deps)
    inputs = depset(ctx.files._swiglib, transitive = [inputs])
    inputs = depset(ctx.files.toolchain_deps, transitive = [inputs])
    swig_include_dirs = depset(_get_repository_roots(ctx, inputs))
    swig_include_dirs = depset(sorted([f.dirname for f in ctx.files._swiglib]), transitive = [swig_include_dirs])
    args = [
        "-c++",
        "-python",
        "-module",
        module_name,
        "-o",
        ctx.outputs.cc_out.path,
        "-outdir",
        ctx.outputs.py_out.dirname,
    ]
    args += ["-l" + f.path for f in ctx.files.swig_includes]
    args += ["-I" + i for i in swig_include_dirs.to_list()]
    args += [src.path]
    outputs = [ctx.outputs.cc_out, ctx.outputs.py_out]
    ctx.actions.run(
        executable = ctx.executable._swig,
        arguments = args,
        inputs = inputs.to_list(),
        outputs = outputs,
        mnemonic = "PythonSwig",
        progress_message = "SWIGing " + src.path,
    )
    return struct(files = depset(outputs))

_py_wrap_cc = rule(
    attrs = {
        "srcs": attr.label_list(
            mandatory = True,
            allow_files = True,
        ),
        "swig_includes": attr.label_list(
            allow_files = True,
        ),
        "deps": attr.label_list(
            allow_files = True,
            providers = [CcInfo],
        ),
        "toolchain_deps": attr.label_list(
            allow_files = True,
        ),
        "module_name": attr.string(mandatory = True),
        "py_module_name": attr.string(mandatory = True),
        "_swig": attr.label(
            default = Label("@swig//:swig"),
            executable = True,
            cfg = "host",
        ),
        "_swiglib": attr.label(
            default = Label("@swig//:templates"),
            allow_files = True,
        ),
    },
    outputs = {
        "cc_out": "%{module_name}.cc",
        "py_out": "%{py_module_name}.py",
    },
    implementation = _py_wrap_cc_impl,
)


def tf_py_wrap_cc(
        name,
        srcs,
        swig_includes = [],
        deps = [],
        copts = [],
        version_script = None,
        **kwargs):
    """Builds a Python extension module."""
    module_name = name.split("/")[-1]

    # Convert a rule name such as foo/bar/baz to foo/bar/_baz.so
    # and use that as the name for the rule producing the .so file.
    cc_library_name = "/".join(name.split("/")[:-1] + ["_" + module_name + ".so"])
    cc_library_pyd_name = "/".join(
        name.split("/")[:-1] + ["_" + module_name + ".pyd"],
    )
    extra_deps = []
    _py_wrap_cc(
        name = name + "_py_wrap",
        srcs = srcs,
        module_name = module_name,
        py_module_name = name,
        swig_includes = swig_includes,
        toolchain_deps = ["@bazel_tools//tools/cpp:current_cc_toolchain"],
        deps = deps + extra_deps,
    )
    if not version_script:
        version_script = select({
            "@local_config_cuda//cuda:darwin": clean_dep("//tensorflow:tf_exported_symbols.lds"),
            "//conditions:default": clean_dep("//tensorflow:tf_version_script.lds"),
        })
    vscriptname = name + "_versionscript"
    _append_init_to_versionscript(
        name = vscriptname,
        is_version_script = select({
            "@local_config_cuda//cuda:darwin": False,
            "//conditions:default": True,
        }),
        module_name = module_name,
        template_file = version_script,
    )
    extra_linkopts = select({
        "@local_config_cuda//cuda:darwin": [
            "-Wl,-exported_symbols_list,$(location %s.lds)" % vscriptname,
        ],
        clean_dep("//tensorflow:windows"): [],
        "//conditions:default": [
            "-Wl,--version-script",
            "$(location %s.lds)" % vscriptname,
        ],
    })
    extra_deps += select({
        "@local_config_cuda//cuda:darwin": [
            "%s.lds" % vscriptname,
        ],
        clean_dep("//tensorflow:windows"): [],
        "//conditions:default": [
            "%s.lds" % vscriptname,
        ],
    })

    tf_cc_shared_object(
        name = cc_library_name,
        srcs = [module_name + ".cc"],
        copts = copts + if_not_windows([
            "-Wno-self-assign",
            "-Wno-sign-compare",
            "-Wno-write-strings",
        ]),
        linkopts = extra_linkopts,
        linkstatic = 1,
        deps = deps + extra_deps,
        **kwargs
    )
    native.genrule(
        name = "gen_" + cc_library_pyd_name,
        srcs = [":" + cc_library_name],
        outs = [cc_library_pyd_name],
        cmd = "cp $< $@",
    )
    native.py_library(
        name = name,
        srcs = [":" + name + ".py"],
        srcs_version = "PY2AND3",
        data = select({
            clean_dep("//tensorflow:windows"): [":" + cc_library_pyd_name],
            "//conditions:default": [":" + cc_library_name],
        }),
    )


genrule(
    name = "libapi",
    srcs = [],
    outs = [],
    cmd = "",
    data = [],
    deps = ["//api:capi"]
)


