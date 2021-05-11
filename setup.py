import os
from glob import glob
from setuptools import setup

exec(open('marvis/version.py').read())

setup(name='marvis',
      version=__version__,
      scripts=glob(os.path.join('scripts', '*')),
      description='VMD Magic',
      author='Andrew White, Glen Hocky',
      author_email='andrew.white@rochester.edu',
      url='https://github.com/whitead/marvis',
      license='MIT',
      packages=['marvis'],
      install_requires=[
          'click',
          'openai',
          'rcsbsearch',
          'google-cloud-speech',
          'importlib_resources'],
      test_suite='tests',
      zip_safe=True,
      includes_package_data=True,
      package_data={'nmrdata': ['marvis/tcl/*.tcl']},
      entry_points='''
        [console_scripts]
        marvis=marvis.main:main
        vmt=marvis.main:text
            '''
      )
