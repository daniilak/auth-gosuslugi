import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auth_gosuslugi",
    version="0.0.2",
    author="Daniil Agniashvili",
    author_email="dortos123456@gmail.com",
    description="Authorization on sites through gosuslugi using requests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daniilak/auth-gosuslugi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux"
    ],
    install_requires=['requests','urllib3', 'pip_system_certs'],
    python_requires='>3.5',
)