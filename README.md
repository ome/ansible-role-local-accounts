Local Accounts
==============

[![Actions Status](https://github.com/ome/ansible-role-local-accounts/workflows/Molecule/badge.svg)](https://github.com/ome/ansible-role-local-accounts/actions)
[![Ansible Role](https://img.shields.io/ansible/role/41887.svg)](https://galaxy.ansible.com/ome/local_accounts/)

Create or remove local user accounts.


Role Variables
--------------

- `local_accounts_create`: A list of dictionaries containing information on the user to be created (default: empty).
  Each item may contain the following fields:
  - `user`: username (required)
  - `uid`: user-ID (required)
  - `groups`: optional list of groups to be appended to the user's default groups
  - `password`: optional password hash, only set if the user is created in this invocation
  - `sshpubkey`: optional SSH public key to be added to the authorized_keys file
  - `sshexclusive`: optional, if `True` and `sshpubkey` is specified, removes all other non-specified keys. Otherwise, appends the the key to any existing keys if not already present. Default: `False.
  - `require_first_password`: optional, if `True` attempt to force a newly created user to change their password on first login, default `False`.
- `local_accounts_groups`: A list of dictionaries containing information on the group to be created (default: empty).
  Each item must contain the following fields:
  - `gid`: group-ID
  - `group`: group-name

UIDs and GIDs are currently required since this role is intended for use across multiple connected nodes.

For example, if you set `sshpubkey`, omit `password` and set `require_first_password: True` the user should be able to log in over SSH using their key, and should be prompted to set a password immediately.
However, failing to set a password will also allow any existing user to `su` to the new users without a password.

- `local_accounts_delete`: List of usernames to be deleted (default: empty). Home directories will not be removed.


Example Playbook
----------------

    - hosts: localhost
      roles:
      - role: ome.local_accounts
        local_accounts_create:
        - user: test1
          uid: 1001
        - user: test2
          uid: 1002
          groups: wheel
          sshpubkey: "ssh-rsa XXXXX"
        local_accounts_delete:
        - user3
        - user4

Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
