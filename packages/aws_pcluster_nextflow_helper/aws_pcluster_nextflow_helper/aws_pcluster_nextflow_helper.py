"""Main module."""

from datetime import datetime
import dataclasses
from pydantic.dataclasses import dataclass
from typing import List, Any, AnyStr, TypedDict, Tuple
import pandas as pd
import tempfile
import os
import shutil
import subprocess

nextflow_log_fields = [
    "attempt",
    "complete",
    "container",
    "cpus",
    "disk",
    "duration",
    "env",
    "error_action",
    "exit",
    "hash",
    "inv_ctxt",
    "log",
    "memory",
    "module",
    "name",
    "native_id",
    "pcpu",
    "peak_rss",
    "peak_vmem",
    "pmem",
    "process",
    "queue",
    "rchar",
    "read_bytes",
    "realtime",
    "rss",
    "scratch",
    "script",
    "start",
    "status",
    "stderr",
    "stdout",
    "submit",
    "syscr",
    "syscw",
    "tag",
    "task_id",
    "time",
    "vmem",
    "vol_ctxt",
    "wchar",
    "workdir",
    "write_bytes",
]


def sanity_check(workdir: str):
    return


def remap_columns(df: pd.DataFrame):
    new_columns = {}
    for column in df.columns:
        new_column = column.strip()
        new_column = new_column.replace(" ", '_')
        new_columns[column] = new_column
    return new_columns


@dataclass
class NextflowLog:
    columns: List = dataclasses.field(default_factory=lambda: nextflow_log_fields)
    workdir: str = os.getcwd()

    def log(self) -> pd.DataFrame:
        with tempfile.NamedTemporaryFile(suffix='.tsv') as fh:
            subprocess.run([f'nextflow log > {fh.name}'], shell=True, cwd=self.workdir)
            data = pd.read_csv(fh.name, sep="\t")
            data = data.rename(columns=remap_columns(data))
        return data

    def log_run(self, run_name) -> pd.DataFrame:
        with tempfile.NamedTemporaryFile(suffix='.tsv') as fh:
            print(f'Run Name: {run_name}')
            subprocess.run([f"nextflow log {run_name} -f {','.join(nextflow_log_fields)} >  {fh.name}"],
                           shell=True,
                           cwd=self.workdir)
            t = open(fh.name, 'r').readlines()
            print(t)
            data = pd.read_csv(fh.name, sep="\t", header=None)
        return data

    def log_all_runs(self):
        runs_df = self.log()
        dataframes = []
        for run in runs_df['RUN_NAME']:
            run_df = self.log_run(run)
            dataframes.append(run_df)

        return pd.concat(dataframes)


l = NextflowLog()
data = l.log()
df = l.log_all_runs()
