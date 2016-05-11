import os
import sys
import subprocess


def setup_config(cfg):
    if sys.platform in ['darwin', 'win32']:
        user = ''
        pwd = os.getcwd()
        if sys.platform == 'win32':
            pwd = pwd.replace(':\\', '/')
            pwd = pwd.replace('\\', '/')
    else:
        uid = os.getuid()
        gid = os.getegid()
        user = ' -u {}:{}'.format(uid, gid)
        pwd = os.getcwd()
    cfg['run'] = cfg['run'].format(user=user, pwd=pwd)
    return cfg


CONFIG = setup_config({
    'repo': 'furiousluke/laa:latest',
    'run': 'docker run{user} -it --rm -v {pwd}:/usr/local/app furiousluke/laa:latest',
    'plink': '/usr/local/plink/plink',
    'convert': '/usr/local/bin/convert.py',
    'fast': '/usr/local/fastStructure/structure.py',
    'choosek': '/usr/local/fastStructure/chooseK.py',
})


def local(cmd):
    print(cmd)
    subprocess.check_call(cmd, shell=True)


def init():
    local('docker pull {repo}'.format(**CONFIG))


def convert(input, output, recombined=False, format='csv'):
    opts = []
    if not recombined:
        opts.append('-m')
    if format == 'csv':
        opts.append('-c')
    if opts:
        opts = ' ' + ' '.join(opts)
    else:
        opts = ''
    cmd = '{run} python {convert}{1} {0}'.format(input, opts, **CONFIG)
    if output:
        cmd += ' -o ' + output
    local(cmd)


def plink(input):
    cmd = '{run} {plink} --file {0} --out {0} --make-bed --noweb'.format(input, **CONFIG)
    local(cmd)


def fast(input, output, k):
    opts = ['--input=' + input, '--output=' + output, '-K', str(k)]
    opts = ' '.join(opts)
    cmd = '{run} python {fast} {0}'.format(opts, **CONFIG)
    local(cmd)


def choosek(input, output, maxk, skipfast=False):
    if not skipfast:
        for ii in xrange(1, int(maxk) + 1):
            fast(input, output, k=ii)
    cmd = '{run} python {choosek} --input={0}'.format(output, **CONFIG)
    local(cmd)


def analyse(input, maxk, **kwargs):
    plink(input)
    choosek(input, input, maxk, **kwargs)


def all(input, maxk, **kwargs):
    conv_output = os.path.splitext(input)[0]
    convert(input, conv_output + '.ped', **kwargs)
    analyse(conv_output, maxk, **kwargs)
