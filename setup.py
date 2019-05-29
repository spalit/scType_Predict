from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='scType_Predict',
      version='0.0.1',
      description='Demo project',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent'
      ],
      url='https://github.com/theislab',
      author='SubarnaPalit',
      author_email='subarna.palit@helmholtz-muenchen.de',
      keywords='core package',
      license='MIT',
      packages=[],
      install_requires=["keras","tensorflow","numpy"],
      include_package_data=True,
      zip_safe=False)
