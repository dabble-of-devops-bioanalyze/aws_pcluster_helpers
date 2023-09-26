import dataclasses
import os
from pathlib import Path
from typing import Union

from pydantic import BaseModel, computed_field

ENV_PCLUSTER_CONFIG_FILE = "PCLUSTER_CONFIG_FILE"
ENV_INSTANCE_TYPE_MAPPINGS_FILE = "INSTANCE_TYPE_MAPPINGS_FILE"
ENV_INSTANCE_TYPES_DATA_FILE = "INSTANCE_TYPES_DATA_FILE"


class PClusterConfigFiles(BaseModel):
    # pcluster_config_file: str = "/opt/parallelcluster/shared/cluster-config.yaml"
    # instance_name_type_mappings_file: str = "/opt/slurm/etc/pcluster/instance_name_type_mappings.json"
    # instance_types_data_file: str = "/opt/parallelcluster/shared/instance-types-data.json"

    @computed_field
    @property
    def pcluster_config_file(self) -> Union[str, Path]:
        return os.environ.get(
            ENV_PCLUSTER_CONFIG_FILE, "/opt/parallelcluster/shared/cluster-config.yaml"
        )

    @computed_field
    @property
    def instance_name_type_mappings_file(self) -> Union[str, Path]:
        return os.environ.get(
            ENV_INSTANCE_TYPE_MAPPINGS_FILE,
            "/opt/slurm/etc/pcluster/instance_name_type_mappings.json",
        )

    @computed_field
    @property
    def instance_types_data_file(self) -> Union[str, Path]:
        return os.environ.get(
            ENV_INSTANCE_TYPES_DATA_FILE,
            "/opt/parallelcluster/shared/instance-types-data.json",
        )
