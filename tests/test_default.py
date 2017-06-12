import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_user_alice(User, File):
    u = User('alice')
    assert u.exists
    assert u.uid == 2020
    assert u.groups == ['alice']
    assert not File('/home/test1/.ssh').exists


def test_user_bob(File, User):
    u = User('bob')
    assert u.exists
    assert u.uid == 1010
    assert sorted(u.groups) == ['bob', 'wheel']

    f = File('/home/bob/.ssh/authorized_keys')
    assert f.exists
    assert f.user == 'bob'
    assert f.group == 'bob'
    assert f.mode == 0o600
    assert f.content == 'ssh-rsa XXXXX \n'
