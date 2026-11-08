"""For colcon, pip uses pyproject.toml"""

from setuptools import setup

setup(python_requires=">=3.10",
      data_files=[("share/ament_index/resource_index/packages", ["resource/robot1"]),
                  ("share/robot1", ["package.xml"])])
