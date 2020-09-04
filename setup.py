from setuptools import setup, find_packages

setup(
    name='alpheios_tokenizer',
    version="0.0.1",
    packages=find_packages(exclude=["examples", "tests"]),
    url='https://github.com/alpheios-project/tokenizer',
    license='GNU GPL',
    author='Bridget Almas',
    author_email='balmas@gmail.com',
    description='Tokenizer for Alpheios',
    test_suite="tests",
    install_requires=[
        "click",
        "flask==1.1.2",
        "Flask-Cache==0.13.1",
        "flask-cors==2.0.0",
        "Flask-Restful==0.3.8",
        "requests>=2.8.1",
        "requests-cache==0.4.9",
        "lxml<5.0.0",
        "marshmallow",
        "spacy==2.3.2",
    ],
    tests_require=[
    ],
    include_package_data=True,
    zip_safe=False
)
