from distutils.core import setup
setup(name='patho_pdb_domain',
		version='0.0.1',
		py_modules=['MOAD_PDBBIN','extracts','ligand_from_pdb'],
		scripts=['MOAD_PDBBIN/MOAD.py','MOAD_PDBBIN/filter_MOAD.py', 'MOAD_PDBBIN/toMolar.py', 'MOAD_PDBBIN/PDBBIND.py', 'extracts/extract_ligand_from_pdb.py'
			 ,'extracts/extract_pdb_from_domain.py','extracts/protein_id_extract_to_uniprot.py'],

		requires=['requests','argparse'],

		author='Federico Serral',
		license='MIT license',
		author_email='fedeserral92@gmail.com',
		description='Extract true ligands',
		url='https://github.com/fedeserral/patho_pdb_domain',
		long_description='',
		)
