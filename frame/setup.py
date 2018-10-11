from setuptools import setup, find_packages

setup(name='rango-frame',
      version='0.1',
      packages=find_packages(),
      include_package_data=True,
      author='zhulinfeng',
      author_email='zhulinfeng@yunjingit.com',
      license='N/A',
      description='A restful django framework, wrapped all common features',
      url='http://www.yunjingit.com/',
      long_description='',
      platforms=['Any', ],
      install_requires=('django', 'djangorestframework'))
