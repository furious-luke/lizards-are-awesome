import os
from setuptools import setup, find_packages

setup(
    name='lizards-are-awesome',
    version='0.2',
    author='Luke Hodkinson',
    author_email='furious.luke@gmail.com',
    maintainer='Luke Hodkinson',
    maintainer_email='furious.luke@gmail.com',
    url='https://github.com/furious-luke/lizards-are-awesome',
    description='',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='BSD',
    packages=find_packages(),
    scripts=['laa/scripts/laa'],
    include_package_data=True,
    install_requires=['setuptools'],
    zip_safe=False,
)
