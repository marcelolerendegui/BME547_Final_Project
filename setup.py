from setuptools import setup, find_packages

setup(
    name='Image Processing Core',
    packages=['core'],
    version='1.0.0',
    description='Image Processing Core',
    author=','.join([
        'Marcelo Lerendegui',
        'WeiHsien Lee',
        'Yihang Xin',
    ]),
    author_email=','.join([
        'marcelo@lerendegui.com',
        'weihsien.lee@duke.edu',
        'yihang.xin@duke.edu'
    ]),
    url='https://github.com/marcelolerendegui/BME547_Final_Project',
    include_package_data=True,
    install_requires=[
    ],
)


setup(
    name='Image Processing Server',
    packages=['server'],
    version='1.0.0',
    description='Image Processing Server',
    author=','.join([
        'Marcelo Lerendegui',
        'WeiHsien Lee',
        'Yihang Xin',
    ]),
    author_email=','.join([
        'marcelo@lerendegui.com',
        'weihsien.lee@duke.edu',
        'yihang.xin@duke.edu'
    ]),
    url='https://github.com/marcelolerendegui/BME547_Final_Project',
    include_package_data=True,
    install_requires=[
        'flask',
        'scikit-image',
        'pymodm',
        'numpy',
    ],
)

setup(
    name='Image Processing Client',
    packages=['client'],
    version='1.0.0',
    description='Image Processing Client',
    author=','.join([
        'Marcelo Lerendegui',
        'WeiHsien Lee',
        'Yihang Xin',
    ]),
    author_email=','.join([
        'marcelo@lerendegui.com',
        'weihsien.lee@duke.edu',
        'yihang.xin@duke.edu'
    ]),
    url='https://github.com/marcelolerendegui/BME547_Final_Project',
    include_package_data=True,
    install_requires=[
        'requests',
        'PyQt5',
        'PyQt5-sip',
        'scikit-image',
        'numpy',
    ],
)
