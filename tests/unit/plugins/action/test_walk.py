# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import re
import unittest

from ansible.playbook.task import Task
from ansible.template import Templar

from ansible_collections.ansible.snmp.plugins.action.walk import ActionModule


try:
    from unittest.mock import MagicMock  # pylint:disable=syntax-error
except ImportError:
    from mock import MagicMock  # pyright: ignore[reportMissingModuleSource]


class TestWalk(unittest.TestCase):
    def setUp(self):
        task = MagicMock(Task)
        # Ansible > 2.13 looks for check_mode in task
        task.check_mode = False
        play_context = MagicMock()
        # Ansible <= 2.13 looks for check_mode in play_context
        play_context.check_mode = False
        connection = MagicMock()
        fake_loader = {}
        templar = Templar(loader=fake_loader)
        self._plugin = ActionModule(
            task=task,
            connection=connection,
            play_context=play_context,
            loader=fake_loader,
            templar=templar,
            shared_loader_obj=None,
        )
        self._plugin._task.action = "get"
        self._task_vars = {
            "inventory_hostname": "mockdevice",
            "ansible_snmp_timeout": 5000000,
            "ansible_connection": "ansible.snmp.v2c",
            "ansible_snmp_community": "rocommunity",
        }

    def test_walk(self):
        """Check passing invalid argspec"""
        self._plugin._task.args = {"oids": {"oid": "RFC1213-MIB::ifTable"}}
        result = self._plugin.run(task_vars=self._task_vars)
        self.assertTrue(result["failed"])
        self.assertIn("missing required arguments: after", result["msg"])
