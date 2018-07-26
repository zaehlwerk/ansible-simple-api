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
# along with Ansible Simple API. If not, see <http://www.gnu.org/licenses/>.
#
"""ansible_simple_api/callback.py: Results callback plugin"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase

class ResultCallback(CallbackBase):
    """A sample callback plugin collecting the results"""

    def __init__(self):
        super(ResultCallback, self).__init__()
        self.results = {}

    def default_action(self, result):
        try:
            host_results = self.results[result._host.name]
        except KeyError:
            host_results = []
            self.results[result._host.name] = host_results
        host_results.append((result.task_name, result._result))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.default_action(result)

    def v2_runner_on_ok(self, result, **kwargs):
        self.default_action(result)

    def v2_runner_on_skipped(self, result):
        self.default_action(result)

    def v2_runner_on_unreachable(self, result):
        self.default_action(result)
