from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'krishs_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='krish',
    maintainer_email='krish@example.com',
    description='ECTE477 lab nodes.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'move_tb3_circle = krishs_pkg.move_tb3_circle:main',
            'lidar_sub = krishs_pkg.lidar_sub:main',
            'publisher_node = krishs_pkg.publisher_node:main',
            'subscriber_node = krishs_pkg.subscriber_node:main',
            'move_to_wall = krishs_pkg.move_to_wall:main',
            'add_two_ints_server = krishs_pkg.add_two_ints_server:main',
            'add_two_ints_client = krishs_pkg.add_two_ints_client:main',
            'fibonacci_server = krishs_pkg.fibonacci_server:main',
            'fibonacci_client = krishs_pkg.fibonacci_client:main',
        ],
    },
)
