from setuptools import setup, find_packages

setup(
    name='soft_pwm',  # This should be unique on PyPI
    version='0.1.1',
    description='A Python library for software-based PWM control using WiringPi',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yassine Moukil',
    author_email='matrixmoukil7@gmail.com',
    url='https://github.com/Electro-Gamma/soft_pwm_lib',
    packages=find_packages(),
    install_requires=[
        'wiringpi'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
