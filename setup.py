from setuptools import setup, find_packages

setup(
    name='qrcode-generator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'qrcode',
        'pillow',
    ],
)
