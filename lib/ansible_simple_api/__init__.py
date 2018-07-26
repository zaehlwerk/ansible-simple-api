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
"""ansible_simple_api/__init__.py: Ansible Simple API"""

def Ansible(*args, **kwargs):
    """Unfortunately any import from Ansible takes some time (~1s) and
    also creates (via import of ansible.constants) a temporary directory
    which has to be cleaned up. Therefore we suspend importing and wrap
    `Ansible` into a function which imports and calls it.

    With PEP 562 (Python 3.7) this can be replaced with
    module's __getattr__ """

    from .api import Ansible
    return Ansible(*args, **kwargs)
