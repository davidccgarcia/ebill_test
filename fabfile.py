from __future__ import with_statement
from time import time

from fabric.api import cd, run, env
from fabric.decorators import task
from fabric.contrib.files import exists

env.use_ssh_config = True
env.hosts = ['adminebill']

releases_dir = '~/html/releases'
git_branch = 'master'
git_repo = 'git@github.com:davidccgarcia/ebill.git'
repo_dir = '~/html/repo'
persist_dir = '~/html/persist'
next_release = "%(time).0f" % {'time': time()}
current_release = '~/html/current'

@task
def deploy():
    init()
    update_git()
    create_release()
    build_site()
    swap_symlinks()

def init():
    if not exists(releases_dir):
        run('mkdir -p %s' % releases_dir)

    if not exists(repo_dir):
        run('git clone -b %s %s %s' % (git_branch, git_repo, repo_dir))

    if not exists('%s/storage' % persist_dir):
        run('mkdir -p %s/storage/app/public' % persist_dir)
        run('mkdir -p %s/storage/framework/cache' % persist_dir)
        run('mkdir -p %s/storage/framework/sessions' % persist_dir)
        run('mkdir -p %s/storage/framework/views' % persist_dir)
        run('mkdir -p %s/storage/framework/testing' % persist_dir)
        run('mkdir -p %s/storage/logs' % persist_dir)

def update_git():
    with cd(repo_dir):
        run('git checkout %s' % git_branch)
        run('git pull origin %s' % git_branch)

def create_release():
    release_into = '%s/%s' % (releases_dir, next_release)
    run('mkdir -p %s' % release_into)
    with cd(repo_dir):
        run('git archive --worktree-attributes %s | tar -x -C %s' % (git_branch, release_into))

def build_site():
    with cd('%s/%s' % (releases_dir, next_release)):
        run('composer install')

def swap_symlinks():
    release_into = '%s/%s' % (releases_dir, next_release)
    
    run('ln -nfs %s/.env %s/.env' % (persist_dir, release_into))
    run('rm -rf %s/storage' % release_into)
    run('ln -nfs %s/storage %s/storage' % (persist_dir, release_into))

    run('ln -nfs %s %s' % (release_into, current_release))
    run('sudo service php7.2-fpm reload')