import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloud-weather",
    version="0.0.1",
    author="Deepak Natanmai",
    description="Simple Package to connect with weather.com endpoints and get quick info",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent",
        'Topic :: Weather',
    ],
    keywords='Weather api crawling scraping',
    install_requires=['requests','BeautifulSoup','argparse'],
    python_requires='>=3.6',
)