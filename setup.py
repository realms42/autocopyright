from setuptools import setup, find_packages

setup(
    name='autocopyright',
    version='1.0.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List your project's dependencies here
        # e.g., 'requests >= 2.24.0',
    ],
    # # Optional metadata
    # author='Your Name',
    # author_email='your.email@example.com',
    # description='A short description of your project.',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    # url='https://github.com/realms42/autocopyright',
    # classifiers=[
    #     # Choose your license as you wish
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.8',
    #     'Programming Language :: Python :: 3.9',
    #     'Programming Language :: Python :: 3.10',
    # ],
)