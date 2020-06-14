from setuptools import setup, find_packages

version = '1.0'

setup(name='nose2-kflag',
      version=version,
      description='nose2 plugin to only run tests which match a given substring',
      long_description=open('README.rst').read() + '\n' +
                       open('CHANGES.rst').read(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      keywords='nose2 plugin kflag test-name-pattern patterns filter',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='https://github.com/stefanholek/nose2-kflag',
      project_urls={
          'Bug Tracker': 'https://github.com/stefanholek/nose2-kflag/issues',
          'Source Code': 'https://github.com/stefanholek/nose2-kflag',
      },
      license='BSD-2-Clause',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      test_suite='nose2_kflag.tests',
      install_requires=[
          'nose2',
      ],
)
