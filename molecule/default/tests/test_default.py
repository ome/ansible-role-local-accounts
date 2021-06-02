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
    assert f.content_string.rstrip() == 'ssh-rsa XXXXX'


def test_ssh_non_exclusive(host):
    u = host.user('user1')
    assert u.exists
    assert u.uid == 1001

    f = host.file('/home/user1/.ssh/authorized_keys')
    assert f.exists
    assert f.user == 'user1'
    assert f.group == 'user1'
    assert f.mode == 0o600
    keys = [x.rstrip() for x in f.content_string.splitlines()]
    assert keys == ['ssh-rsa 1001', 'ssh-rsa new 1001']


def test_ssh_exclusive(host):
    u = host.user('user2')
    assert u.exists
    assert u.uid == 1002

    f = host.file('/home/user2/.ssh/authorized_keys')
    assert f.exists
    assert f.user == 'user2'
    assert f.group == 'user2'
    assert f.mode == 0o600
    assert f.content_string.rstrip() == 'ssh-rsa new 1002'


def test_precreated_users(host):
    u = host.user('user5')
    assert u.exists
    assert u.uid == 1005


def test_deleted_users(host):
    u = host.user('user3')
    assert not u.exists
    u = host.user('user4')
    assert not u.exists
