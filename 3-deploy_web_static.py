#!/usr/bin/python3
"""A Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers"""
from fabric.api import local
from datetime import datetime
from os import makedirs
from fabric.api import env, put, run, runs_once
import os


env.user = 'ubuntu'
env.hosts = ['54.236.26.138', '3.84.158.55']


@runs_once
def do_pack():
    """Fabric script that generates a .tgz archive
    from the contents of the web_static folder of your AirBnB Clone repo"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(timestamp)
    archive_path = "versions/{}".format(archive_name)

    makedirs("versions", exist_ok=True)
    result = local("tar -czvf {} web_static".format(archive_path))

    if result.succeeded:
        return archive_path
    else:
        return None


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


def deploy():
    """creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
