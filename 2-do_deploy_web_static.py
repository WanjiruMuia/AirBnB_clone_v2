#!/usr/bin/python3
"""Fabric script to generate a .tgz archive from the contents of the web_static
folder of the AirBnB Clone repo and deploy it to web servers.
"""

from fabric.api import env, run, put
from os.path import exists
from datetime import datetime

# Servers
env.hosts = ['<IP web-01>', 'IP web-02']


def do_pack():
    """Packs the contents of web_static folder into a .tgz archive"""
    try:
        time_now = datetime.now().strftime('%Y%m%d%H%M%S')
        file_path = "versions/web_static_{}.tgz".format(time_now)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(file_path))
        return file_path
    except:
        return None


def do_deploy(archive_path):
    """Deploys the archive to web servers"""
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        # Upload archive to /tmp/ directory on the web server
        put(archive_path, "/tmp/")
        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        run("mkdir -p /data/web_static/releases/{}/".format(folder_name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, folder_name))
        run("rm /tmp/{}".format(file_name))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(folder_name, folder_name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(folder_name))
        run("rm -rf /data/web_static/current")
        # Create a new symbolic link /data/web_static/current linked to the new version
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(folder_name))
        return True
    except:
        return False
        
