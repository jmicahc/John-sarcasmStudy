import shutil
import os

for d in os.listdir('Materials/'):
    if d.startswith('.'): continue
    if d.startswith('odd'): continue
    replacement_d = '_'.join(['odd'] + d.split('_')[1:] )
    for f in os.listdir('Materials/' +d):
        if f.startswith('.'): continue
        if f.startswith('odd'): continue
        print f
        s_dir = f[:f.index('.')]
        if int(f[-6:-4]) % 2 != 0 and 'sin' in f:
            os.mkdir('Materials/' + replacement_d + '/' + s_dir)
            shutil.copyfile('Materials/' + d + '/' + f,'Materials/' + replacement_d + '/' + s_dir + '/' + f)
            os.remove('Materials/' + d + '/' + f)
        elif int(f[-6:-4]) % 2 == 0 and 'sar' in f:
            os.mkdir('Materials/' + replacement_d + '/' + s_dir)
            shutil.copyfile('Materials/' + d + '/' + f,'Materials/' + replacement_d + '/' + s_dir + '/' + f)
            os.remove('Materials/' + d + '/' + f)
        else:
            os.mkdir('Materials/' + d + '/' + s_dir)
            shutil.copyfile('Materials/' + d + '/' + f, 'Materials/' +
                            d + '/' + s_dir + '/' + f)
            os.remove('Materials/' + d + '/' + f)

