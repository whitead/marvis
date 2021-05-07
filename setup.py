import os
from glob import glob
from setuptools import setup

exec(open('vmdmagic/version.py').read())

setup(name='vmdmagic',
      version=__version__,
      scripts=glob(os.path.join('scripts', '*')),
      description='VMD Magic',
      author='Andrew White, Glen Hocky',
      author_email='andrew.white@rochester.edu',
      url='https://github.com/whitead/vmdmagic',
      license='MIT',
      packages=['vmdmagic'],
      install_requires=[
          'click',
          'openai',
          'rcsbsearch',
          'google-cloud-speech',
          'importlib_resources'],
      test_suite='tests',
      zip_safe=True,
      includes_package_data=True,
      package_data={'nmrdata': ['vmdmagic/tcl/*.tcl']},
      entry_points='''
        [console_scripts]
        vmdmagic=vmdmagic.main:main
        vmdmagic-text=vmdmagic.main:text
            '''
      )
