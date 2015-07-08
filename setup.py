from setuptools import find_packages, setup


version = '0.9.0.python2'


setup(
    name='django-pgcrypto-fields',
    packages=find_packages(),
    include_package_data=True,
    version=version,
    license='BSD',
    description='Encrypted fields dealing with pgcrypto postgres extension.',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Security :: Cryptography',
    ],
    author='Incuna Ltd, coldmind',
    author_email='admin@incuna.com, me@asokolovskiy.com',
    url='https://github.com/coldmind/django-pgcrypto-fields',
)
