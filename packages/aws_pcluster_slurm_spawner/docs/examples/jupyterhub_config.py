#################################################################
# Custom Configuration
#################################################################

import json
import os
import batchspawner
import jupyter_rsession_proxy
import getpass
import os
from traitlets import Integer, Unicode, Float, Dict
from aws_pcluster_slurm_spawner import (PClusterSlurmSpawner, pcluster_spawner_template_paths)

#################################################################
# Networking
#################################################################

c.JupyterHub.bind_url = 'http://0.0.0.0:3000'
c.Application.log_level = 'DEBUG'
c.Spawner.default_url = '/lab'

# Hub IP
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 3001

c.ConfigurableHTTPProxy.api_url = 'http://0.0.0.0:3002'

c.JupyterHub.db_url = 'sqlite:///jupyterhub.sqlite'

c.JupyterHub.cookie_secret_file = 'jupyterhub_cookie_secret'

#################################################################
# Authentication
#################################################################

c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'
c.PAMAuthenticator.open_sessions = False
c.Authenticator.admin_users = set(['ec2-user', 'user2135'])

#################################################################
# Batchspawner
#################################################################

c.Spawner.debug = True
c.BatchSpawnerBase.debug = True
## Sometimes we have to wait awhile for a node to spin up
c.Spawner.http_timeout = 60
c.Spawner.start_timeout = 500

# ------------------------------------------------------------------------------
# BatchSpawnerBase configuration
#   Providing default values that we may omit in the profiles
# ------------------------------------------------------------------------------

c.BatchSpawnerBase.req_partition = 'basic'
c.BatchSpawnerBase.req_runtime = '1:00:00'
c.BatchSpawnerBase.req_options = ''

import shlex

import batchspawner
from jupyterhub.spawner import LocalProcessSpawner
from jinja2 import Environment, BaseLoader

from aws_pcluster_slurm_spawner import (PClusterSlurmSpawner, pcluster_spawner_template_paths)

c.JupyterHub.spawner_class = PClusterSlurmSpawner
# c.JupyterHub.template_paths = [pcluster_spawner_template_paths]

c.JupyterHub.allow_named_servers = True
