import os
import sys
from setuptools import setup, find_packages

# 读取README文件
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取版本信息
version = "1.0.0"

setup(
    name="windows-kms-activator",
    version=version,
    author="KMS Activator Team",
    author_email="support@kms-activator.com",
    description="Windows KMS激活工具 - 一键激活Windows系统",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kms-activator/windows-kms-activator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=[
        # 使用标准库，无额外依赖
    ],
    entry_points={
        "console_scripts": [
            "kms-activator=kms_activator:main",
        ],
        "gui_scripts": [
            "kms-activator-gui=kms_activator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.ico", "*.png", "*.md"],
    },
    data_files=[
        ("", ["README.md", "方法指导.md"]),
    ],
    keywords="windows activation kms license",
    project_urls={
        "Bug Reports": "https://github.com/kms-activator/windows-kms-activator/issues",
        "Source": "https://github.com/kms-activator/windows-kms-activator",
        "Documentation": "https://github.com/kms-activator/windows-kms-activator/blob/main/README.md",
    },
)