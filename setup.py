import os
from setuptools import find_packages, setup


install_requires = [
    'django>=1.8',
    'wagtail>=1.2'
]

setup(
    name='wagtail-seo',
    version='0.1.0',
    description='Search engine optimization helpers for Django Wagtail.',
    author='Rob Moorman',
    author_email='rob@moori.nl',
    url='https://github.com/moorinteractive/wagtail-seo',
    license='MIT',
    install_requires=install_requires,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ]
)
