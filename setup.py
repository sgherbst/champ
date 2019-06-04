from setuptools import setup, find_packages

setup(
    name="champ",
    version="0.0.1",
    description='Channel modeling in Python',
    url='https://github.com/sgherbst/champ',
    author='Steven Herbst',
    author_email='sherbst@stanford.edu',
    packages=['champ'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'mpltools',
        'scikit-rf'
    ]
)
