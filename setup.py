from pathlib import Path
import re
import setuptools

setup_dir = Path(__file__).resolve().parent

version = re.search( r'__version__ = "(.*)"', Path(setup_dir, 'calcure/__main__.py').open().read())
if version is None:
    raise SystemExit("Could not determine version to use")
version = version.group(1)

setuptools.setup(
    name='calcure',
    author='Roman Anufriev',
    author_email='anufriev.roman@protonmail.com',
    url='https://github.com/anufrievroman/calcure',
    description='Modern TUI calendar and task manager',
    long_description=Path(setup_dir, 'README.md').open().read(),
    long_description_content_type='text/markdown',
    license='MIT',
    entry_points={
        "console_scripts": [
            "calcure = calcure.__main__:cli"
        ]
    },
    install_requires=['holidays', 'jdatetime', 'ics'],
    version=version,
    python_requires='~=3.7',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    packages=["calcure", "calcure.translations"],
    include_package_data=True,
)
