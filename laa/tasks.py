import os
import sys
import subprocess


def setup_config(cfg):
    if sys.platform in ['darwin', 'win32']:
        user = ''
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


def init(args):
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
        cmd += ' -o ' + output[0]
    local(cmd)


def plink(input):
    cmd = '{run} {plink} --file {0} --out {0} --make-bed --noweb'.format(input, **CONFIG)
    local(cmd)


def fast(input, output, **kwargs):
    opt_map = {
        'K': '-K ',
    }
    opts = ['--input=' + input, '--output=' + output]
    opts.extend([opt_map.get(k, '--' + k + '=') + str(v) for k, v in kwargs.items()])
    opts = ' '.join(opts)
    cmd = '{run} python {fast} {0}'.format(opts, **CONFIG)
    local(cmd)


def choosek(input, output, maxk, **kwargs):
    skipfast = kwargs.pop('skipfast', '').lower()
    if skipfast not in ['true', 'yes', '1', 'y']:
        for ii in xrange(1, int(maxk) + 1):
            print green('Running with K=%d ... '%ii)
            fast(input, output, K=ii, **kwargs)
    print green('Choosing K ... ')
    cmd = '{run} python {choosek} --input={0}'.format(output, **CONFIG)
    output = local(cmd, capture=True)
    print red(output)


def analyse(input, maxk, **kwargs):
    plink(input)
    choosek(input, input, maxk, **kwargs)


def all(input, maxk, **kwargs):
    conv_output = os.path.splitext(input)[0]
    convert(input, conv_output + '.ped', **kwargs)
    analyse(conv_output, maxk, **kwargs)
