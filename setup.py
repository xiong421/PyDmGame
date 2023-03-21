# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/17 22:57
@Auth ： 大雄
@File ：setup.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
from setuptools import setup
import os

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
README = os.path.join(CUR_DIR, "README.md")
with open("README.md", "r", encoding="utf-8") as fd:
    long_description = fd.read()
setup(
    name="PyDmGame",
    version="0.0.4",
    description="Python version of dm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xiong421/PyDmGame/",
    author="da xiong",
    author_email="270207756@qq.com",
    install_requires=[
        "opencv-python>=4.3.0.38",
        "pywin32>=305",
    ],
    packages=['PyDmGame',
              'PyDmGame/model',
              'PyDmGame/modular',
              'PyDmGame/modular/basic',
              'PyDmGame/modular/display_',
              'PyDmGame/modular/km_',
              'PyDmGame/modular/ocr_'],
    include_package_data = True,
    # package_data={'': ['*.dll','*.txt','*.pdiparams','*.info','*.pdmodel','*.exe']},

    python_requires='>=3.6',
    keywords='windows game dm',
)
