# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/17 22:57
@Auth ： 大雄
@File ：setup.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import setuptools
import os

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
README = os.path.join(CUR_DIR, "README.md")
with open("README.md", "r", encoding="utf-8") as fd:
    long_description = fd.read()
setuptools.setup(
    name="PyDmGame",
    version="0.0.2",
    description="Python version of dm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://space.bilibili.com/470514128?spm_id_from=333.788.0.0",
    author="da xiong",
    author_email="270207756@foxmail.com",
    install_requires=[
        "opencv-python>=4.3.0.38",
        "pywin32>=305",
    ],
    packages=['PyDmGame', "PyDmGame/modular", "PyDmGame/model", "PyDmGame/tests", "PyDmGame/model",
              "PyDmGame/modular/display_", "PyDmGame/modular/keyboard_", "PyDmGame/modular/mouse_", ],
    python_requires='>=3.6',
    keywords='windows game dm',
)
