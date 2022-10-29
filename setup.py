from setuptools import setup, find_packages

try:
    README = open('README.rst').read()
except Exception:
    README = None

setup(
    author='Brandon Taylor',
    author_email='alsoicode@gmail.com',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
    description='Database-driven way to put your Django site into maintenance mode.',
    include_package_data=True,
    install_requires=['django'],
    license='APL',
    long_description=README,
    name='django-maintenancemode-2',
    packages=find_packages(exclude=['testproject']),
    url='https://github.com/alsoicode/django-maintenancemode-2',
    version=__import__('maintenancemode').__version__,
    zip_safe=False
)
