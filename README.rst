==================
Ansible Simple API
==================

This is very simple wrapper around Ansible's API with sensible defaults.

Here is an example:

>>> from ansible_simple_api import Ansible
>>> ansible = Ansible(connection='local', inventory='localhost,')
>>> ansible.run('localhost', 'debug', msg="Hello Ansible Simple API")
{localhost: {'msg': 'Hello Ansible Simple API', '_ansible_verbose_always': True, '_ansible_no_log': False, 'changed': False}}
