from distutils.core import setup

setup(
    name='rapidsms-authsites',
    version='0.1',
    license="BSD",

    requires = ["rapidsms (>=0.9.6a)"],

    description='An extension for associating django Users and Groups, as well as RapidSMS Contacts and Messages, with a particular site (without modifying the existing models).',
    long_description=open('README.rst').read(),
    author='David McCann',
    author_email='david.a.mccann@gmail.com',

    url='http://github.com/daveycrockett/rapidsms-authsites',
    download_url='http://github.com/daveycrockett/rapidsms-authsites/downloads',

    include_package_data=True,

    packages=['authsites'],

    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
