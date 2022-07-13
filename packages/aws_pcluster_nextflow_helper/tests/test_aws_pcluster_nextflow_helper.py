#!/usr/bin/env python

"""Tests for `aws_pcluster_nextflow_helper` package."""


import unittest
from click.testing import CliRunner

from aws_pcluster_nextflow_helper import aws_pcluster_nextflow_helper
from aws_pcluster_nextflow_helper import cli


class TestAws_pcluster_nextflow_helper(unittest.TestCase):
    """Tests for `aws_pcluster_nextflow_helper` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'aws_pcluster_nextflow_helper.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
