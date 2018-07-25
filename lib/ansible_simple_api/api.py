# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 by Gregor Giesen
#
# This file is part of Ansible Simple API.
#
# Ansible Simple API is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# Ansible Simple API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible Simple API. If not, see <http://www.gnu.org/licenses/>.#
"""ansible_simple_api/api.py: Simple access to Ansible API"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import atexit
import shutil

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible import constants as C

from .callback import ResultCallback

@atexit.register
def cleanup_temp():
    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

class Ansible:
    """Easy access to Ansible API

    Example:
    >>> ansible = Ansible()
    >>> results = ansible.run("host1,host2", module="debug", msg="foo")
    >>> for host, result in results.items():
    ...     print(host, result['msg'])
    host1 foo
    host2 foo

    """

    def __init__(self, connection=C.DEFAULT_TRANSPORT,
                 inventory=C.DEFAULT_HOST_LIST, forks=10):
        self.connection = connection
        self.module_path = []
        self.forks = forks
        self.become = None
        self.become_method = None
        self.become_user = None
        self.check = False
        self.diff = False

        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader,
                                          sources=inventory)
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory)

        result_callback = ResultCallback()
        tqm = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self,
            passwords=None,
            stdout_callback=result_callback)

        @atexit.register
        def cleanup_tqm():
            tqm.cleanup()

        self.tqm = tqm
        self.results = result_callback.results

    def reset(self):
        if self.tqm is not None:
            self.tqm.cleanup()
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory)

        result_callback = ResultCallback()
        self.tqm = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self,
            passwords=None,
            stdout_callback=result_callback,
        )
        self.results = result_callback.results

    def run(self, hosts: str, module: str, _arg=None, **kwargs):
        """Runs a single action on hosts"""
        results = self.run_play(
            None, hosts, tasks=[
                dict(action=dict(
                    module=module,
                    args=_arg if _arg else kwargs))])
        return dict((host, host_results[-1][1])
                    for host, host_results in results.items())

    def run_play(self, name: str, hosts: str, tasks=[], roles=[],
            gather_facts: bool=False):
        """runs a play on hosts"""
        play = Play.load(
            dict(
                name=name,
                hosts=hosts,
                tasks=tasks,
                roles=roles,
                gather_facts='yes' if gather_facts else 'no'),
            variable_manager=self.variable_manager, loader=self.loader)
        self.tqm.run(play)
        return self.results
