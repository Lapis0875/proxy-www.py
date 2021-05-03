from setuptools import setup, find_packages

with open('./README.md', mode='rt', encoding='utf-8') as f:
    long_description: str = f.read()

# Setup module
setup(
    # Module name
    name='proxy-www',
    # Module version
    version='1.0.1',
    # License - MIT!
    license='MIT',
    # Author (Github username)
    author='Lapis0875',
    # Author, Lapis0875`s email.
    author_email='lapis0875@kakao.com',
    # Short description
    description='Port library of proxy-www in npm (https://github.com/justjavac/proxy-www)',
    # Long description in REAMDME.md
    long_description_content_type='text/markdown',
    long_description=long_description,
    # Project url
    url='https://github.com/Lapis0875/proxy-www.py',
    # Include module directory 'chronous'
    packages=find_packages(),
    # Dependencies : This project use module 'colorlog', so add requirements.
    install_requires=['3.7.4.post0'],
    # Module`s python requirement
    python_requires='>=3.6',
    # Keywords about the module
    keywords=['aiohttp', 'network', 'http request', 'asynchronous', 'asyncio'],
    # Tags about the module
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
)
