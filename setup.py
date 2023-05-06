from setuptools import setup, find_packages

requires = [
    'flask',
    'spotipy',
    'htmlSlib',
    'requests',
    'requests_html',
    'beautifulsoup4',
    'youtube_dl',
    'pathlib',
    'pandas'
]

setup(
    name='Muvie',
    version='1.0',
    description='Application that recommends movies based on Spotify songs',
    author='Zachary Fishman',
    author_email='zachmfishman@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
