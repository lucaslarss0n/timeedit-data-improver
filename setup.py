from setuptools import setup, find_packages

setup(
    name='csv_processor',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'process_csv=your_script:main',  # Replace 'your_script' with the actual script filename without the .py extension
        ],
    },
)
