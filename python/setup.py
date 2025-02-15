# Copyright (c) 2021-2022, NVIDIA CORPORATION & AFFILIATES
#
# SPDX-License-Identifier: BSD-3-Clause

import os
import sys

from Cython.Build import cythonize
from setuptools import setup, Extension, find_packages

# this is tricky: sys.path gets overwritten at different stages of the build
# flow, so we need to hack sys.path ourselves...
source_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(source_root, 'builder'))
import utils  # this is builder.utils


# Use README for the project long description
with open(os.path.join(source_root, "README.md")) as f:
    long_description = f.read()


# Get test requirements
with open(os.path.join(source_root, "tests/requirements.txt")) as f:
    tests_require = f.read().split('\n')


# Runtime dependencies
# - cuTENSOR version is constrained in the cutensornet-cuXX package, so we don't
#   need to list it
install_requires = [
    'numpy',
    # 'cupy', # TODO: use "cupy-wheel" once it's stablized, see https://github.com/cupy/cupy/issues/6688
    # 'torch', # <-- PyTorch is optional; also, the PyPI version does not support GPU...
    f'custatevec-cu{utils.cuda_major_ver}~=1.1',   # ">=1.1.0,<2"
    f'cutensornet-cu{utils.cuda_major_ver}~=2.0',  # ">=2.0.0,<3"
    ]


# Note: the extension attributes are overwritten in build_extension()
ext_modules = [
    Extension(
        "cuquantum.custatevec.custatevec",
        sources=["cuquantum/custatevec/custatevec.pyx"],
    ),
    Extension(
        "cuquantum.cutensornet.cutensornet",
        sources=["cuquantum/cutensornet/cutensornet.pyx"],
    ),
    Extension(
        "cuquantum.utils",
        sources=["cuquantum/utils.pyx"],
        include_dirs=[os.path.join(utils.cuda_path, 'include')],
    ),
]


cmdclass = {
    'build_ext': utils.build_ext,
    'bdist_wheel': utils.bdist_wheel,
}

if utils.cuda_major_ver == '11':
    cuda_classifier = [
        "Environment :: GPU :: NVIDIA CUDA :: 11.0",
        "Environment :: GPU :: NVIDIA CUDA :: 11.1",
        "Environment :: GPU :: NVIDIA CUDA :: 11.2",
        "Environment :: GPU :: NVIDIA CUDA :: 11.3",
        "Environment :: GPU :: NVIDIA CUDA :: 11.4",
        "Environment :: GPU :: NVIDIA CUDA :: 11.5",
        "Environment :: GPU :: NVIDIA CUDA :: 11.6",
        "Environment :: GPU :: NVIDIA CUDA :: 11.7",
        "Environment :: GPU :: NVIDIA CUDA :: 11.8",
    ]
else:
    cuda_classifier = None

# TODO: move static metadata to pyproject.toml
setup(
    name=f"cuquantum-python-cu{utils.cuda_major_ver}",
    version=utils.cuqnt_py_ver,
    description="NVIDIA cuQuantum Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NVIDIA/cuQuantum",
    author="NVIDIA Corporation",
    author_email="cuquantum-python@nvidia.com",
    license="BSD-3-Clause",
    license_files = ('LICENSE',),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Environment :: GPU :: NVIDIA CUDA",
    ] + cuda_classifier,
    ext_modules=cythonize(ext_modules,
        verbose=True, language_level=3,
        compiler_directives={'embedsignature': True}),
    packages=find_packages(include=['cuquantum', 'cuquantum.*']),
    package_data={"": ["*.pxd", "*.pyx", "*.py"],},
    zip_safe=False,
    python_requires='>=3.8',
    install_requires=install_requires,
    tests_require=install_requires+tests_require,
    cmdclass=cmdclass,
)
