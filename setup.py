from setuptools import setup


setup(
    name='django-exmodel',
    version='0.0.2',
    description='Makes your Django models extendable.',
    long_description=open('README.rst').read(),
    author='Mikko Hellsing',
    author_email='mikko@aino.com',
    url='http://github.com/sorl/django-exmodel',
    packages=['exmodel'],
    install_requires=['Django>=1.5', 'six>=1.9.0'],
    license='ICS',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
    ],
    zip_safe=False
)
