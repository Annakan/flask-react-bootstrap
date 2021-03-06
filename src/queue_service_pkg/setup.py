from setuptools import setup
import os

###########################
# Readme and longdesc
###########################
MODULE_NAME = 'queue_service'
try:
    from pypandoc import convert

    def read_md(f):
        return convert(f, 'rst')

except ImportError:
    convert = None
    print(
        "warning: pypandoc module not found, could not convert Markdown to RST"
    )

    def read_md(f):
        return open(f, 'r', encoding='utf-8').read()  # noqa
README = os.path.join(os.path.dirname(__file__), 'README.md')


###########################
# Version
###########################

def get_version(version_tuple):
    # additional handling of a,b,rc tags, this can
    # be simpler depending on your versioning scheme
    if not isinstance(version_tuple[-1], int):
        return '.'.join(
            map(str, version_tuple[:-1])
        ) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))


# path to the packages __init__ module in project
# source tree
init = os.path.join(
    os.path.dirname(__file__), '%s' % MODULE_NAME,
    '__init__.py'
)
version_line = list(
    filter(lambda l: l.startswith('VERSION'), open(init, encoding="utf-8"))
)[0]

# VERSION is a tuple so we need to eval its line of code.
# We could simply import it from the package but we
# cannot be sure that this package is importable before
# finishing its installation
VERSION = get_version(eval(version_line.split('=')[-1]))


###########################
# requirements
###########################

def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs(*f):
    return list(filter(None, [strip_comments(l) for l in open(
        os.path.join(os.getcwd(), *f), encoding='utf-8').readlines()]))


setup(
    name=MODULE_NAME,
    version=VERSION,
    # (...)
    description="Flask+ React + SocketIO Python 3 Demo ",
    long_description=read_md(README),
    install_requires=reqs('requirements.txt'),
    extras_require={
        # 'dev': ['pydevd'],
    },
    entry_points={
        'console_scripts': ['queueservice_run=queue_service.console:main',
                            ],
    },
    author='X³',
    author_email='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ],
)