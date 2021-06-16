About cudatoolkit-dev
=====================

Home: https://developer.nvidia.com

Package license: [LicenseRef-NVIDIA-End-User-License-Agreement](https://docs.nvidia.com/cuda/eula/index.html)

Feedstock license: [BSD-3-Clause](https://github.com/conda-forge/cudatoolkit-dev-feedstock/blob/master/LICENSE.txt)

Summary: Develop, Optimize and Deploy GPU-accelerated Apps

Development: https://developer.nvidia.com/cuda-toolkit

Documentation: https://developer.nvidia.com/cuda-toolkit

The NVIDIA CUDA Toolkit provides a development environment for creating
high performance GPU-accelerated applications. With the CUDA Toolkit,
you can develop, optimize and deploy your applications on GPU-accelerated
embedded systems, desktop workstations, enterprise data centers,
cloud-based platforms and HPC supercomputers. The toolkit includes
GPU-accelerated libraries, debugging and optimization tools,
a C/C++ compiler and a runtime library to deploy your application.
This package consists of a post-install script that downloads and
installs the full cuda toolkit(compiler, libraries, with the exception of cuda drivers).


Differences between this package and cudatoolkit from the main Anaconda channel
-------------------------------------------------------------------------------

When you install cudatoolkit-dev, in addition to libraries; you get the compiler (nvcc), the profiler (nvprof), etc. 
In other words, you get the exact outcome as what you would get when installing cudatoolkit 
by following installation steps from https://developer.nvidia.com/cuda-downloads.

On the other hand, when you install cudatoolkit from the main Anaconda channel, all you get is a set of 
pre-packaged libraries (no compiler, no profiler, etc).


Current build status
====================


<table>
    
  <tr>
    <td>Azure</td>
    <td>
      <details>
        <summary>
          <a href="https://dev.azure.com/conda-forge/feedstock-builds/_build/latest?definitionId=5537&branchName=master">
            <img src="https://dev.azure.com/conda-forge/feedstock-builds/_apis/build/status/cudatoolkit-dev-feedstock?branchName=master">
          </a>
        </summary>
        <table>
          <thead><tr><th>Variant</th><th>Status</th></tr></thead>
          <tbody><tr>
              <td>linux_64_python3.6.____cpython</td>
              <td>
                <a href="https://dev.azure.com/conda-forge/feedstock-builds/_build/latest?definitionId=5537&branchName=master">
                  <img src="https://dev.azure.com/conda-forge/feedstock-builds/_apis/build/status/cudatoolkit-dev-feedstock?branchName=master&jobName=linux&configuration=linux_64_python3.6.____cpython" alt="variant">
                </a>
              </td>
            </tr><tr>
              <td>linux_64_python3.7.____cpython</td>
              <td>
                <a href="https://dev.azure.com/conda-forge/feedstock-builds/_build/latest?definitionId=5537&branchName=master">
                  <img src="https://dev.azure.com/conda-forge/feedstock-builds/_apis/build/status/cudatoolkit-dev-feedstock?branchName=master&jobName=linux&configuration=linux_64_python3.7.____cpython" alt="variant">
                </a>
              </td>
            </tr><tr>
              <td>linux_64_python3.8.____cpython</td>
              <td>
                <a href="https://dev.azure.com/conda-forge/feedstock-builds/_build/latest?definitionId=5537&branchName=master">
                  <img src="https://dev.azure.com/conda-forge/feedstock-builds/_apis/build/status/cudatoolkit-dev-feedstock?branchName=master&jobName=linux&configuration=linux_64_python3.8.____cpython" alt="variant">
                </a>
              </td>
            </tr><tr>
              <td>linux_64_python3.9.____cpython</td>
              <td>
                <a href="https://dev.azure.com/conda-forge/feedstock-builds/_build/latest?definitionId=5537&branchName=master">
                  <img src="https://dev.azure.com/conda-forge/feedstock-builds/_apis/build/status/cudatoolkit-dev-feedstock?branchName=master&jobName=linux&configuration=linux_64_python3.9.____cpython" alt="variant">
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </details>
    </td>
  </tr>
</table>

Current release info
====================

| Name | Downloads | Version | Platforms |
| --- | --- | --- | --- |
| [![Conda Recipe](https://img.shields.io/badge/recipe-cudatoolkit--dev-green.svg)](https://anaconda.org/conda-forge/cudatoolkit-dev) | [![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/cudatoolkit-dev.svg)](https://anaconda.org/conda-forge/cudatoolkit-dev) | [![Conda Version](https://img.shields.io/conda/vn/conda-forge/cudatoolkit-dev.svg)](https://anaconda.org/conda-forge/cudatoolkit-dev) | [![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/cudatoolkit-dev.svg)](https://anaconda.org/conda-forge/cudatoolkit-dev) |

Installing cudatoolkit-dev
==========================

Installing `cudatoolkit-dev` from the `conda-forge` channel can be achieved by adding `conda-forge` to your channels with:

```
conda config --add channels conda-forge
conda config --set channel_priority strict
```

Once the `conda-forge` channel has been enabled, `cudatoolkit-dev` can be installed with:

```
conda install cudatoolkit-dev
```

It is possible to list all of the versions of `cudatoolkit-dev` available on your platform with:

```
conda search cudatoolkit-dev --channel conda-forge
```


About conda-forge
=================

[![Powered by NumFOCUS](https://img.shields.io/badge/powered%20by-NumFOCUS-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](http://numfocus.org)

conda-forge is a community-led conda channel of installable packages.
In order to provide high-quality builds, the process has been automated into the
conda-forge GitHub organization. The conda-forge organization contains one repository
for each of the installable packages. Such a repository is known as a *feedstock*.

A feedstock is made up of a conda recipe (the instructions on what and how to build
the package) and the necessary configurations for automatic building using freely
available continuous integration services. Thanks to the awesome service provided by
[CircleCI](https://circleci.com/), [AppVeyor](https://www.appveyor.com/)
and [TravisCI](https://travis-ci.com/) it is possible to build and upload installable
packages to the [conda-forge](https://anaconda.org/conda-forge)
[Anaconda-Cloud](https://anaconda.org/) channel for Linux, Windows and OSX respectively.

To manage the continuous integration and simplify feedstock maintenance
[conda-smithy](https://github.com/conda-forge/conda-smithy) has been developed.
Using the ``conda-forge.yml`` within this repository, it is possible to re-render all of
this feedstock's supporting files (e.g. the CI configuration files) with ``conda smithy rerender``.

For more information please check the [conda-forge documentation](https://conda-forge.org/docs/).

Terminology
===========

**feedstock** - the conda recipe (raw material), supporting scripts and CI configuration.

**conda-smithy** - the tool which helps orchestrate the feedstock.
                   Its primary use is in the construction of the CI ``.yml`` files
                   and simplify the management of *many* feedstocks.

**conda-forge** - the place where the feedstock and smithy live and work to
                  produce the finished article (built conda distributions)


Updating cudatoolkit-dev-feedstock
==================================

If you would like to improve the cudatoolkit-dev recipe or build a new
package version, please fork this repository and submit a PR. Upon submission,
your changes will be run on the appropriate platforms to give the reviewer an
opportunity to confirm that the changes result in a successful build. Once
merged, the recipe will be re-built and uploaded automatically to the
`conda-forge` channel, whereupon the built conda packages will be available for
everybody to install and use from the `conda-forge` channel.
Note that all branches in the conda-forge/cudatoolkit-dev-feedstock are
immediately built and any created packages are uploaded, so PRs should be based
on branches in forks and branches in the main repository should only be used to
build distinct package versions.

In order to produce a uniquely identifiable distribution:
 * If the version of a package **is not** being increased, please add or increase
   the [``build/number``](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html#build-number-and-string).
 * If the version of a package **is** being increased, please remember to return
   the [``build/number``](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html#build-number-and-string)
   back to 0.

Feedstock Maintainers
=====================

* [@AgrawalAmey](https://github.com/AgrawalAmey/)
* [@andersy005](https://github.com/andersy005/)
* [@scopatz](https://github.com/scopatz/)
* [@xmnlab](https://github.com/xmnlab/)

