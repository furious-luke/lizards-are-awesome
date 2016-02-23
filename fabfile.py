from fabric.api import local, task, hide
from fabric.colors import red, green


CONFIG = {
    'repo': 'furiousluke/faa:latest',
    'run': 'docker run -it --rm -v `pwd`:/usr/local/app katja',
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
            print green('done')
    print green('Choosing K ... ')
    cmd = '{run} python {choosek} --input={0}'.format(outfn, **CONFIG)
    output = local(cmd, capture=True)
    print red(output)
    print green('done')


@task
def analyse(infn, outfn, maxk, **kwargs):
    plink(infn)
    choosek(infn, infn, maxk, **kwargs)


@task
def all(infn, outfn, maxk, **kwargs):
    convert(infn, infn, **kwargs)
    analyse(infn, outfn, maxk, **kwargs)


@task
def cli():
    cmd = '{run} sh'.format(**CONFIG)
    local(cmd)
