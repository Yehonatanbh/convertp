from setuptools import setup, find_packages


def get_long_description():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='convertp',
    version='0.1',
    author='yehon',
    author_email='yehonatanbh1@gmail.com',
    description='Convert RTP stream to audio files.',
    long_description=get_long_description(),
    packages=['convertp'],
    # url='https://github.com/Yehonatanbh/convertp',
    license='GNU General Public License v2.0',
    install_requires=['pyshark', 'pydub'],
    python_requires='>=3.8.5'
)
