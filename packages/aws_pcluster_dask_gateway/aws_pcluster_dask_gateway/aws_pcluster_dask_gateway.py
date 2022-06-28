from __future__ import annotations
from dask_gateway_server.options import Options, Select

from aws_pcluster_helpers.models.sinfo import (SInfoTable, SinfoRow)
import functools
import os

from jinja2 import Environment, BaseLoader
from pydantic.dataclasses import dataclass
import dataclasses
from typing import List, Any, TypedDict, Dict, Optional
from typing import ForwardRef
from devtools import PrettyFormat, pprint, pformat, debug
import json
import yaml

from aws_pcluster_helpers import (
    PClusterConfig,
    InstanceTypesData,
    PClusterInstanceTypes,
    InstanceTypesMappings,
    size_in_gib,
)

from aws_pcluster_helpers.models.instance_types_data import (
    PClusterInstanceTypes,
    InstanceTypesMappings,
)

from aws_pcluster_helpers.models import sinfo
from aws_pcluster_helpers import (
    PClusterConfig,
    InstanceTypesData,
    PClusterInstanceTypes,
    InstanceTypesMappings,
    size_in_gib,
)
from aws_pcluster_helpers.utils.logging import setup_logger
from aws_pcluster_helpers.models.config import PClusterConfigFiles

from traitlets import Unicode, default

from dask_gateway_server.backends.jobqueue.slurm import SlurmClusterConfig, SlurmBackend
from dask_gateway_server.options import Options, Select, String

"""
Docs

https://gateway.dask.org/cluster-options.html
https://gateway.dask.org/install-jobqueue.html

"""


@dataclass
class DaskGatewaySlurmConfig(sinfo.SInfoTable):
    @functools.cached_property
    def profiles(self):
        profiles = {}
        for sinfo_row in self.rows:
            label = f"P: {sinfo_row.queue}, I: {sinfo_row.ec2_instance_type}, CPU: {sinfo_row.vcpu}, Mem: {sinfo_row.mem}"
            profiles[label] = {
                "worker_cores": sinfo_row.vcpu,
                "worker_memory": sinfo_row.mem,
                "constraint": sinfo_row.constraint,
                "queue": sinfo_row.queue,
            }
        return profiles

    def __post_init__(self):
        return


class PClusterBackend(SlurmBackend):
    constraint = Unicode("", help="The job instance type constraint.", config=True)
    default_profile: str = None

    @functools.cached_property
    def cluster_options(self):
        dask_gateway_slurm_config = DaskGatewaySlurmConfig()
        profile_names = list(dask_gateway_slurm_config.profiles.keys())
        if self.default_profile:
            default_profile = self.default_profile
        else:
            default_profile = profile_names[0]
        Options(
            Select(
                "profile",
                profile_names,
                default=default_profile,
                label="Cluster Profile",
            ),
            String(
                "environment",
                label="Conda Environment"
            ),
            handler=lambda options: dask_gateway_slurm_config.profiles[options.profile],
        )
        return

    def get_submit_cmd_env_stdin(self, cluster, worker=None):
        cmd = [self.submit_command, "--parsable", "--job-name=dask-gateway"]
        if cluster.config.partition:
            cmd.append("--partition=" + cluster.config.partition)
        if cluster.config.account:
            cmd.account("--account=" + cluster.config.account)
        if cluster.config.qos:
            cmd.extend("--qos=" + cluster.config.qos)
        if cluster.config.constraint:
            cmd.extend("--constraint=" + cluster.config.constraint)

        if worker:
            cpus = cluster.config.worker_cores
            # mem = slurm_format_memory(cluster.config.worker_memory)
            log_file = "dask-worker-%s.log" % worker.name
            script = "\n".join(
                [
                    "#!/bin/sh",
                    cluster.config.worker_setup,
                    " ".join(self.get_worker_command(cluster, worker.name)),
                ]
            )
            env = self.get_worker_env(cluster)
        else:
            cpus = cluster.config.scheduler_cores
            # mem = slurm_format_memory(cluster.config.scheduler_memory)
            log_file = "dask-scheduler-%s.log" % cluster.name
            script = "\n".join(
                [
                    "#!/bin/sh",
                    cluster.config.scheduler_setup,
                    " ".join(self.get_scheduler_command(cluster)),
                ]
            )
            env = self.get_scheduler_env(cluster)

        staging_dir = self.get_staging_directory(cluster)

        cmd.extend(
            [
                "--chdir=" + staging_dir,
                "--output=" + os.path.join(staging_dir, log_file),
                "--cpus-per-task=%d" % cpus,
                # "--mem=%s" % mem,
                "--export=%s" % (",".join(sorted(env))),
            ]
        )

        return cmd, env, script

# @dataclass
# class DaskGatewayPClusterProfiles()
# A mapping from profile name to configuration overrides

# Expose `profile` as an option, valid values are 'small', 'medium', or
# 'large'. A handler is used to convert the profile name to the
# corresponding configuration overrides.
# c.Backend.cluster_options = Options(
#     Select(
#         "profile",
#         ["small", "medium", "large"],
#         default="medium",
#         label="Cluster Profile",
#     ),
#     handler=lambda options: profiles[options.profile],
# )
