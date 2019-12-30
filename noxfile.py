import shutil
import os

import nox

nox.options.reuse_existing_virtualenvs = True

PYTHON_VERSIONS = ['3.6', '3.7', '3.8']


@nox.session(python=PYTHON_VERSIONS[-1])
def lint(session):
    """Performs pep8 and security checks."""
    source_code = 'click_params'
    session.install('flake8', 'bandit')
    session.run('flake8', source_code)
    session.run('bandit', '-r', source_code)


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    """Runs the test suite."""
    session.install('click', 'validators', 'pytest', 'pytest-cov', 'pytest-mock')
    session.run('pytest')

    # we notify codecov when the latest version of python is used
    if session.python == PYTHON_VERSIONS[-1] and 'APPVEYOR_URL' not in os.environ:
        session.notify('codecov')


@nox.session
def codecov(session):
    """Runs codecov command to share coverage information on codecov.io"""
    session.install('codecov')
    session.cd('tests')
    session.run('coverage', 'xml', '-i')
    session.run('codecov', '-f', 'coverage.xml')


@nox.session(python=PYTHON_VERSIONS[-1])
def docs(session):
    """Builds the documentation."""
    session.install('mkdocs')
    session.run('mkdocs', 'build', '--clean')


@nox.session
def deploy(session):
    """
    Deploys build on pypi repositories (can be test or production repository).
    Extra arguments passed to nox will be passed to the twine command.
    """
    if not session.posargs and not session.interactive:
        session.error("you don't pass arguments to session and you are not in interactive mode")
    session.install('-U', 'twine', 'setuptools', 'wheel')
    session.run('python', 'setup.py', 'sdist', 'bdist_wheel')
    session.run('twine', 'upload', 'dist/*', *session.posargs)


@nox.session(python=False)
def clean(*_):
    """Since nox take a bit of memory, this command helps to clean nox environment."""
    shutil.rmtree('.nox', ignore_errors=True)
