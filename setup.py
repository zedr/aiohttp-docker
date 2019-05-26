from setuptools import setup



def _get_version():
    with open('VERSION') as fd:
        return fd.read().strip()


setup(
    name='aio-demo',
    version=_get_version(),
    packages=['aio_demo'],
    package_dir={'': 'src'},
    py_modules=['aio_demo.main', 'aio_demo.tests'],
    entry_points={
        'console_scripts': [
            'aio-demo-serve=aio_demo.main:main',
            'aio-demo-test=aio_demo.tests:main'
        ]
    }
)
