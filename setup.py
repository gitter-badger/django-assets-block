import os
from distutils.core import setup
from setuptools import find_packages
VERSION = __import__("assetsblock").__version__
CLASSIFIERS = [
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
]
install_requires = [
    'django>=1.6.6',
]
# taken from django-registration
# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)
for dirpath, dirnames, filenames in os.walk('assetsblock'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[12:] # Strip "assetsblock/" or "assetsblock\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))
setup(
    name="django-assets-block",
    description="Django application to add `assets` tag that accumulate content from all templates involved in output",
    version=VERSION,
    author="Obshtestvo.bg",
    author_email="info@obshtestvo.bg",
    url="https://github.com/obshtestvo-utilities/django-assets-block",
    download_url="https://github.com/obshtestvo-utilities/django-assets-block/.../tgz",
    package_dir={'assetsblock': 'assetsblock'},
    packages=packages,
    package_data={'assetsblock': data_files},
    include_package_data=True,
    install_requires=install_requires,
    classifiers=CLASSIFIERS,
)