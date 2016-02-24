import os
from fabric.api import local, task, hide
from fabric.colors import red, green


CONFIG = {
    'repo': 'furiousluke/laa:latest',
    'run': 'docker run -u=`stat -c "%u:%g" .` -it --rm -v `pwd`:/usr/local/app furiousluke/laa:latest',
    'plink': '/usr/local/plink/plink',
    'convert': '/usr/local/bin/convert.py',
    'fast': '/usr/local/fastStructure/structure.py',
    'choosek': '/usr/local/fastStructure/chooseK.py',
}


@task
def init():
    local('docker pull {repo}'.format(**CONFIG))


@task
def convert(infn, outfn=None, **kwargs):
    opts = []
    if kwargs.get('merge', '').lower() in ['yes', 'true', '1', 'y']:
        opts.append('-m')
    if opts:
        opts = ' ' + ' '.join(opts)
    else:
        opts = ''
    cmd = '{run} python {convert}{1} {0}'.format(infn, opts, **CONFIG)
    if outfn:
        cmd += ' -o ' + outfn
    local(cmd)


@task
def plink(infn):
    cmd = '{run} {plink} --file {0} --out {0} --make-bed --noweb'.format(infn, **CONFIG)
    local(cmd)


@task
def fast(infn, outfn, **kwargs):
    opt_map = {
        'K': '-K ',
    }
    opts = ['--input=' + infn, '--output=' + outfn]
    opts.extend([opt_map.get(k, '--' + k + '=') + str(v) for k, v in kwargs.items()])
    opts = ' '.join(opts)
    cmd = '{run} python {fast} {0}'.format(opts, **CONFIG)
    local(cmd)


@task
def choosek(infn, outfn, maxk, **kwargs):
    skipfast = kwargs.pop('skipfast', '').lower()
    if skipfast not in ['true', 'yes', '1', 'y']:
        for ii in xrange(1, int(maxk) + 1):
            print green('Running with K=%d ... '%ii)
            fast(infn, outfn, K=ii, **kwargs)
    print green('Choosing K ... ')
    cmd = '{run} python {choosek} --input={0}'.format(outfn, **CONFIG)
    output = local(cmd, capture=True)
    print red(output)


@task
def analyse(infn, maxk, **kwargs):
    plink(infn)
    choosek(infn, infn, maxk, **kwargs)


@task
def all(infn, maxk, **kwargs):
    conv_outfn = os.path.splitext(infn)[0]
    convert(infn, conv_outfn + '.ped', **kwargs)
    analyse(conv_outfn, maxk, **kwargs)


@task
def cli():
    cmd = '{run} sh'.format(**CONFIG)
    local(cmd)
