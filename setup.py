from distutils.core import setup
setup(name='',
		version='0.4.1',
		py_modules=['uniprot'],
		scripts=['uniprot'],

		requires=['requests','argparse'],

		author='Jan Rudolph',
		license='MIT license',
		author_email='jan.daniel.rudolph@gmail.com',
		description='Simple interface for uniprot.org',
		url='https://github.com/jdrudolph/uniprot',
		long_description=open('README').read(),
		)
