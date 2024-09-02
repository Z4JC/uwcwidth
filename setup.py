# SPDX-License-Identifier: MIT
from setuptools import setup, Extension

setup(
    name='uwcwidth',
    ext_modules=[Extension("uwcwidth.uwcwidth",
                           sources=["uwcwidth/uwcwidth.pyx"])],
    package_data={'uwcwidth': ['__init__.pxd', 'uwcwidth.pxd', 'tables.pxd']}
)
