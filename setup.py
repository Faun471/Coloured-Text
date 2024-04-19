from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='coloured_text',
    version='1.0',
    description='Colours text in the terminal using color tags.',
    author='Genre Mamanao',
    author_email='mamanaoglenngenre@gmail.com',
    url='https://github.com/Faun471/Coloured-Text.git',
    py_modules=['coloured_text'],
    install_requires=[],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)