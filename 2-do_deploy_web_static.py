#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
from fabric.api import env, put, run
import os

env.user = 'ubuntu'
env.hosts = ['54.236.26.138', '3.84.158.55']


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        filename = os.path.basename(archive_path)
        folder_name = "/data/web_static/releases/{}".format(
                filename.split('.')[0])

        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_name))

        run("mv {}/web_static/* {}/".format(folder_name, folder_name))

        run("rm -rf {}/web_static".format(folder_name))

        run("rm -rf /data/web_static/current")

        run("ln -s {} /data/web_static/current".format(folder_name))

        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False
