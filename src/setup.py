from setuptools import setup, find_packages

setup(
    name='headphones2',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/omerbenamram/headphones2.git',
    license='GPL',
    author='Omer',
    author_email='omerbenamram@gmail.com',
    description='',
    install_requires=['SQLAlchemy', 'flask', 'beets', 'logbook', 'requests', 'sqlalchemy-utils', 'pytest',
                      'huey',
                      'gevent', 'pies', 'nltk', 'simplejson', 'vcrpy', 'BeautifulSoup4'],
    entry_points={
        'console_scripts': [
            'headphones = headphones2.app:main',
        ]
    }
)
