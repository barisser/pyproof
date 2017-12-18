git_repository(
    name = "io_bazel_rules_python",
        remote = "https://github.com/bazelbuild/rules_python.git",
	    commit = "44711d8ef543f6232aec8445fb5adce9a04767f9",
		)


load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories", "pip_import")
pip_repositories()

pip_import(
   name = "pip_libs",
   requirements = "//:requirements.txt",
)

load("@pip_libs//:requirements.bzl", pip_libs_install = "pip_install")
pip_libs_install()


load('@bazel_tools//tools/build_defs/repo:git.bzl', git_repo = 'git_repository')

git_repo(
    name = "io_bazel_rules_pex",
    remote = "https://github.com/benley/bazel_rules_pex.git",
    commit = "bde25c1c1a21f4670fb56ab8111f342f30aca1a9",
)
load("@io_bazel_rules_pex//pex:pex_rules.bzl", "pex_repositories")
pex_repositories()
