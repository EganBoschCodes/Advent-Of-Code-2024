import setuptools

setuptools.setup(
    name='aoc',
    version="0.0.0",
    description='A python package containing solutions for Advent of Code 2024.',
    url='https://github.com/Egan-Bosch-Codes/Advent-Of-Code-2024',
    author='Egan Bosch',
    install_requires=[
        'pandas',
        'python-dotenv',
    ],
    author_email='egan.bosch@madiba.com',
    packages=setuptools.find_packages(include = ["*"]),
    zip_safe=False
)