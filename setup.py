"""Setup script for the discord-messages-dump package."""

from setuptools import setup, find_packages
import os
import re

# Read the version from __init__.py
with open(os.path.join('discord_messages_dump', '__init__.py'), 'r', encoding='utf-8') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

# Read the long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='discord-messages-dump',
    version=version,
    description='A tool to download and save message history from Discord channels',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Discord Messages Dump Team',
    author_email='example@example.com',
    url='https://github.com/yourusername/discord-messages-dump',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.25.0',
        'python-dotenv>=0.15.0',
        'click>=8.0.0',
        'tqdm>=4.62.0',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'discord-dump=discord_messages_dump:cli_main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Communications :: Chat',
        'Topic :: Utilities',
    ],
    keywords='discord, messages, dump, api, cli',
)
