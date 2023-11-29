#import setuptools
#
#setuptools.setup(
#    name="quantlib",
#    version="0.1",
#    description="code lib by HangukQuant",
#    url="#",
#    author="HangukQuant",
#    install_requires=["opencv-python"],
#    author_email="",
#    packages=setuptools.find_packages(),
#    zip_safe=False
#)

import setuptools

setuptools.setup(
    name="quantlib",
    version="0.1",
    description="Code library by HangukQuant",
    url="https://github.com/hangukquant/quantlib",  # Zamijenite s pravim URL-om vašeg projekta
    author="HangukQuant",
    author_email="amarberbic14@gmail.com",  # Stavite svoju e-mail adresu
    install_requires=["opencv-python"],
    packages=setuptools.find_packages(),
    zip_safe=False
)
