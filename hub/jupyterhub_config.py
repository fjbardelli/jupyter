# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
# https://native-authenticator.readthedocs.io/en/stable/options.html

# Configuration file for JupyterHub
import os, nativeauthenticator
c = get_config()  # noqa: F821

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]
image_list = os.environ.get("DOCKER_NOTEBOOK_IMAGE_LIST", "")
c.DockerSpawner.allowed_images = image_list.split(',')

# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.

spawn_cmd = os.environ.get("DOCKER_SPAWN_CMD", "start-singleuser.sh")
c.DockerSpawner.cmd = spawn_cmd

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Explicitly set notebook directory because we'll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.

notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
jupyter_path = os.environ.get("DOCKER_JUPYTER_PATH", "/jupyter")

c.DockerSpawner.notebook_dir = notebook_dir
#c.DockerSpawner.volumes = {'jupyterhub-data': '/home/jovyan'}
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = { jupyter_path + '/notebooks/user-{username}': {"bind": notebook_dir, "mode": "rw"},
                            jupyter_path + '/compartidos': {"bind": '/home/jovyan/compartidos', "mode": "rw"}    
                        }

# Remove containers once they are stopped
c.DockerSpawner.remove = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True
# User containers will access hub by container name on the Docker network
#c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

# Authenticate users with Native Authenticator
#c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"
c.JupyterHub.authenticator_class = 'native'
c.JupyterHub.template_paths = [f"{os.path.dirname(nativeauthenticator.__file__)}/templates/"]

c.LocalAuthenticator.create_system_users = True
# Allow anyone to sign-up without approval
c.NativeAuthenticator.open_signup = True


# Allowed admins
admin = os.environ.get("JUPYTERHUB_ADMIN")
if admin:
    c.Authenticator.admin_users = [admin]
else:
    c.Authenticator.admin_users = {'admin'}

c.JupyterHub.allow_named_servers = True
c.JupyterHub.allow_shutdown = True

# Native Authenticator Config
c.NativeAuthenticator.check_common_password = os.environ.get("JUPYTERHUB_AUTH_CHECKPWD", "F") == "Y"
c.NativeAuthenticator.minimum_password_length = os.environ.get("JUPYTERHUB_AUTH_PWDLEN", 6)
c.NativeAuthenticator.allowed_failed_logins = os.environ.get("JUPYTERHUB_AUTH_FAILLOGIN", 3)
c.NativeAuthenticator.seconds_before_next_try = os.environ.get("JUPYTERHUB_AUTH_NEXTTRY", 1200)
c.NativeAuthenticator.ask_email_on_signup = os.environ.get("JUPYTERHUB_AUTH_2FAC", "F") == "Y"
c.NativeAuthenticator.allow_2fa = os.environ.get("JUPYTERHUB_AUTH_2FAC", "F") == "Y"

