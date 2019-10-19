import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_user_alice(host):
    u = host.user('alice')
    assert u.exists
    assert u.uid == 2020
    assert u.groups == ['alice']
    assert not host.file('/home/test1/.ssh').exists


def test_user_bob(host):
    u = host.user('bob')
    assert u.exists
    assert u.uid == 1010
    assert sorted(u.groups) == ['bob', 'wheel']

    f = host.file('/home/bob/.ssh/authorized_keys')
    assert f.exists
    assert f.user == 'bob'
    assert f.group == 'bob'
    assert f.mode == 0o600
    assert f.content == 'ssh-rsa XXXXX \n'
