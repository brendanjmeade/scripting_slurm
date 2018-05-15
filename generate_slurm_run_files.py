'''
Write files for submission to SLURM queue
Ideal for batch jobs with no dependencies
This is .py clone of Phoebe Devries' .m file
'''
import os

# Constants
RUN_FILE = './run_all.sh'
MEMORY = 1000 # memory per cpu/python run needed (MB)
FOLDER_RUN = 'run_files'
FOLDER_OUT = 'out_files'
FOLDER_ERR = 'err_files'
N_NPZ_FILES = 500

# Create folder for output files
os.mkdir(FOLDER_RUN)

# Write each batch file and run_all.sh
run_file_id = open(RUN_FILE, 'w')

for i in range(0, N_NPZ_FILES):
    filename = '{}'.format(FOLDER_RUN) + '/' + '{:05d}'.format(i) + '.sh'
    fid = open(filename, 'w')
    fid.write('#!/bin/bash\n')
    fid.write('#SBATCH -J ' + '{:05d}'.format(i) + '\n')
    fid.write('#SBATCH -o ' + '{}'.format(FOLDER_OUT) + '/' + '{:05d}'.format(i) + '.out\n')
    fid.write('#SBATCH -e ' + '{}'.format(FOLDER_ERR) + '/' + '{:05d}'.format(i) + '.err\n')
    fid.write('#SBATCH -p meade\n')
    fid.write('#SBATCH -n 1\n')
    fid.write('#SBATCH -t 24-00:00\n')
    fid.write('#SBATCH --mem-per-cpu=' + '{}'.format(MEMORY) + '\n')
    fid.write('python gen_syn_fields.py ' + '{:05d}'.format(i) + '\n')
    fid.close()

    run_file_id.write('sbatch ' + '{}'.format(FOLDER_RUN) + '/' + '{:05d}'.format(i) + '.sh\n')

# Close the run file and make it executable    
run_file_id.close()
os.system('chmod +777 ' + '{}'.format(RUN_FILE))
