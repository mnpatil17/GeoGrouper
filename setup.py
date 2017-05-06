from setuptools import setup

setup(name='geogrouper',
      version='1.0',
      description='Clusters Geo Samples based on their relative relevance to each other',
      url='http://github.com/mnpatil17/GeoGrouper',
      author='Mihir Patil',
      author_email='mihir.patil@berkeley.edu',
      license='BSD',
      packages=['geogrouper'],
	  install_requires=[
          'pandas',
          'edit_distance',
          'numpy'
      ],
      zip_safe=False)