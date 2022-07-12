from setuptools import setup, find_packages

def readme():
    with open('./README.md') as f:
        return f.read()


setup(
    name='actuality',
    version='2022.2.8.6',
    license='MIT',
    author='Idin',
    author_email='py@idin.ca',
    url='https://github.com/idin/actuality',

    keywords='graph computation',
    description='Python library for a natural language learner AI',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    packages=find_packages(exclude=("jupyter_tests", ".idea", ".git")),
    install_requires=[],
    python_requires='~=3.6',
    zip_safe=True
)
