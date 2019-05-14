import setuptools

setuptools.setup(
    name="damgard-jurik",
    version="0.0.1",
    author="Boucher, Govedič, Saowakon, Swanson",
    description="Multi-authority, homomorphic encryption using the Damgard-Jurik cryptosystem.",
    long_description="Multi-authority, homomorphic encryption using the Damgard-Jurik cryptosystem.",
    url="https://github.com/cryptovoting/damgard-jurik",
    packages=setuptools.find_packages(),
    install_requires=[
        'gmpy2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
