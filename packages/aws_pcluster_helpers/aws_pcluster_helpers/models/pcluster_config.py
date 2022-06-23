# generated by datamodel-codegen:
#   filename:  pcluster_config.yml
#   timestamp: 2022-05-24T09:17:46+00:00

from __future__ import annotations

from typing import List

from pydantic import BaseModel
import yaml
import json
import os
from dataclasses import dataclass
from typing import Union, Dict, Any, TypedDict
from pathlib import Path


class Image(BaseModel):
    Os: str
    CustomAmi: str


class Tag(BaseModel):
    Key: str
    Value: str


class Networking(BaseModel):
    ElasticIp: bool
    SubnetId: str
    AdditionalSecurityGroups: List[str]


class Dcv(BaseModel):
    Enabled: bool
    Port: int


class Ssh(BaseModel):
    KeyName: str


class RootVolume(BaseModel):
    Size: int


class EphemeralVolume(BaseModel):
    MountDir: str


class LocalStorage(BaseModel):
    RootVolume: RootVolume
    EphemeralVolume: EphemeralVolume


class S3Acces(BaseModel):
    BucketName: str
    EnableWriteAccess: bool


class Iam(BaseModel):
    S3Access: List[S3Acces]


class OnNodeConfigured(BaseModel):
    Script: str


class CustomActions(BaseModel):
    OnNodeConfigured: OnNodeConfigured


class HeadNode(BaseModel):
    InstanceType: str
    Networking: Networking
    Dcv: Dcv
    Ssh: Ssh
    LocalStorage: LocalStorage
    Iam: Iam
    CustomActions: CustomActions


class CloudWatch(BaseModel):
    Enabled: bool
    RetentionInDays: int


class Logs(BaseModel):
    CloudWatch: CloudWatch


class CloudWatch1(BaseModel):
    Enabled: bool


class Dashboards(BaseModel):
    CloudWatch: CloudWatch1


class Monitoring(BaseModel):
    Logs: Logs
    Dashboards: Dashboards


class FsxLustreSettings(BaseModel):
    StorageCapacity: int
    DeploymentType: str
    DataCompressionType: str


class SharedStorageItem(BaseModel):
    MountDir: str
    Name: str
    StorageType: str
    FsxLustreSettings: FsxLustreSettings


class RootVolume1(BaseModel):
    Size: int


class EphemeralVolume1(BaseModel):
    MountDir: str


class LocalStorage1(BaseModel):
    RootVolume: RootVolume1
    EphemeralVolume: EphemeralVolume1


class ComputeSettings(BaseModel):
    LocalStorage: LocalStorage1


class ComputeResource(BaseModel):
    Name: str
    InstanceType: str
    MinCount: int = 0
    MaxCount: int = 1


class OnNodeConfigured1(BaseModel):
    Script: str


class CustomActions1(BaseModel):
    OnNodeConfigured: OnNodeConfigured1


class S3Acces1(BaseModel):
    BucketName: str
    EnableWriteAccess: bool


class Iam1(BaseModel):
    S3Access: List[S3Acces1]


class Image1(BaseModel):
    CustomAmi: str


class Networking1(BaseModel):
    SubnetIds: List[str]
    AdditionalSecurityGroups: List[str]


class SlurmQueue(BaseModel):
    Name: str
    ComputeSettings: ComputeSettings
    ComputeResources: List[ComputeResource]
    CustomActions: CustomActions1
    Iam: Iam1
    Image: Image1
    Networking: Networking1


class Scheduling(BaseModel):
    Scheduler: str
    SlurmQueues: List[SlurmQueue]


class PClusterConfig(BaseModel):
    Region: str
    Image: Image
    Tags: List[Tag]
    HeadNode: HeadNode
    Monitoring: Monitoring
    SharedStorage: List[SharedStorageItem]
    Scheduling: Scheduling

    @classmethod
    def from_yaml(cls, yaml_file: str) -> PClusterConfig:
        data = yaml.safe_load(open(yaml_file).read())
        return PClusterConfig(**data)
