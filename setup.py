import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="football-statistics",
    version="0.0.3",
    author="Max Leonard",
    author_email="maxhleonard@gmail.com",
    description="Package for centralized football statistics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxhleonard/football",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src","FootballStats":"src/FootballStats"},
    packages=["FootballStats","FootballStats.odds","FootballStats.scraping","FootballStats.objects"],
    package_data={"FootballStats":["data/*"]},
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "beautifulsoup4"
    ]
)