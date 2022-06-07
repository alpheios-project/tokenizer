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
        "apispec<4.0.0",
        "apispec-webframeworks",
        "click<=7.2.0",
        "flask==1.1.4",
        "Flask-Babel",
        "Flask-Cache==0.13.1",
        "flask-cors==3.0.10",
        "flask-marshmallow",
        "gunicorn",
        "jieba==0.42.1",
        "requests>=2.8.1",
        "requests-cache==0.4.9",
        "lxml<5.0.0",
        "marshmallow",
        "pkuseg==0.0.25",
        "spacy==3.1",
        "urllib3",
        "pymorphy2-dicts-ru",
        "pymorphy2-dicts-uk",
        "pymorphy2",
        "pythainlp",
        "pyvi",
        "Jinja2==2.11.3",
        "MarkupSafe<2.1.0"
    ],
    tests_require=[
    ],
    include_package_data=True,
    zip_safe=False
)
