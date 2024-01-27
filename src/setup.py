import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    'matplotlib',
    'scipy',
    'numpy',
]

test_requirements = [
    'pytest',
    # 'pytest-pep8',
    # 'pytest-cov',
]


setuptools.setup(
    name="npp_2d_truss_analysis", # Replace with your own username
    version="0.0.1",
    author="N. Papadakis",
    author_email="npapnet@gmail.com",
    description="A package for truss analysis with inclined roller support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/npapnet/TrussAnalysis2D",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    tests_require=test_requirements,
    python_requires='>=3.10',
    project_urls={
        'Source': 'https://github.com/npapnet/TrussAnalysis2D',
        'Documentation': 'https://npapnet.github.io/TrussAnalysis2D/',  # TODO Update with your GitHub Pages URL
        # 'Documentation': 'https://TrussAnalysis2D.github.io/en/latest/',
        'PyPI': 'https://pypi.org/project/npp_2d_truss_analysis/'

    },
)