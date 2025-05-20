import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Read long descriptions
with open(os.path.join(here, 'README.txt'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt'), encoding='utf-8') as f:
    CHANGES = f.read()

requires = [
    'plaster_pastedeploy',
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'waitress',
    'alembic',
    'pyramid_retry',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
]

tests_require = [
    'WebTest',
    'pytest',
    'pytest-cov',
]

setup(
    name='runlog_backend',
    version='0.1.0',
    description='RUNLOG - Personal Running Log Tracker API',
    long_description=README + '\n\n' + CHANGES,
    long_description_content_type='text/plain',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',  # Tambahkan versi Python targetmu secara spesifik
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: OSI Approved :: MIT License',
    ],
    author='Your Name',  # Ganti dengan nama asli kamu
    author_email='your@email.com',  # Ganti dengan email kamu
    url='https://github.com/yourusername/runlog-backend',  # Update URL repositori kamu
    keywords='web pyramid REST API running tracker',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = runlog_backend:main',
        ],
        'console_scripts': [
            'initialize_runlog_backend_db=runlog_backend.scripts.initialize_db:main',
        ],
    },
)
