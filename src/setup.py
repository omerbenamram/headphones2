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
    install_requires=['SQLAlchemy',
                      'flask',
                      'flask-cache',
                      'redis',
                      'musicbrainzngs',
                      'pyacoustid',
                      'logbook',
                      'requests',
                      'pytest',
                      'huey',
                      'redis',
                      'sqlalchemy-utils',
                      'simplejson', 'vcrpy', 'BeautifulSoup4', 'marshmallow'],
    entry_points={
        'console_scripts': [
            'headphones = headphones2.app:main',
        ]
    }
)
