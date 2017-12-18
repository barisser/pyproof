load("@pip_libs//:requirements.bzl", "requirement")

load(
    "@io_bazel_rules_pex//pex:pex_rules.bzl",
    "pex_binary",
    "pex_library",
    "pex_test",
    "pex_pytest",
)

py_library(
	name="pyproof_lib",
	srcs=glob(["pyproof/*.py"]),
	imports=["."]
	)

py_test(
	name="pyproof_tests",
	srcs=glob(["tests/*.py"])
	)
