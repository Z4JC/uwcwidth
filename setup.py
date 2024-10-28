# SPDX-License-Identifier: MIT
import os
import platform

from setuptools import setup, Extension


DEBUG=(os.getenv('DEBUG') or '').strip().lower() in ['1', 'y', 'true']
MSVC=(platform.platform().startswith('Windows') and
      platform.python_compiler().startswith('MS'))
COMPILE_ARGS=[] if MSVC else (["-g", "-O0", "-UNDEBUG"] if DEBUG else ["-O3"])


def uwcwidth_ext(module, pyx_file):
    return Extension(module,
                     sources=[pyx_file],
                     extra_compile_args=COMPILE_ARGS)


setup(
    name='uwcwidth',
    ext_modules=[uwcwidth_ext("uwcwidth.uwcwidth", "uwcwidth/uwcwidth.pyx")],
    package_data={'uwcwidth': ['__init__.pxd', 'uwcwidth.pxd', 'tables.pxd']}
)
