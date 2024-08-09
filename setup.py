from setuptools import setup, find_packages

setup(
    name="cubemars_lib",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'python-can'
    ],
    author="Nathan Adkins",
    author_email="npa00003@mix.wvu.edu",
    description="Defines classes for controlling cubemars motors",
    license="MIT",
    keywords="actuator robotics",
    url="https://github.com/wvu-urc/dynamixel_lib",   # project homepage
)