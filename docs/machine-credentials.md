# Machine Credentials

Machine Credentials contain the necessary information for logging into remote hosts as well as how to escalate privileges (sudo/su).

| [Managing Machine Credentials](https://docs.datastax.com/en/opscenter/6.7/api/docs/lcm_machine_credential.html#managing-machine-credentials) | URL                                                          |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Get a machine credential object by ID                        | [`GET /api/v2/lcm/machine_credentials/{id}`](https://docs.datastax.com/en/opscenter/6.7/api/docs/lcm_machine_credential.html#method-get-machine-credential-object) |
| Get a list of machine credentials                            | [`GET /api/v2/lcm/machine_credentials/`](https://docs.datastax.com/en/opscenter/6.7/api/docs/lcm_machine_credential.html#method-get-machine-credential-list) |
| Create a machine credential                                  | [`POST /api/v2/lcm/machine_credentials/`](https://docs.datastax.com/en/opscenter/6.7/api/docs/lcm_machine_credential.html#method-post-machine-credential-object) |
| Update a machine credential                                  | [`PUT /api/v2/lcm/machine_credentials/{id}`](https://docs.datastax.com/en/opscenter/6.7/api/docs/lcm_machine_credential.html#method-put-machine-credential-object) |
| Delete a machine credential                                  | [`DELETE /api/v2/lcm/repositories/{id}`](https://docs.datastax.com/en/opscenter/6.7/api/docs/lcm_repository.html#method-delete-repository-object) |

## Machine Credential

```json
{
    "id": <value>,
    "name": <value>,
    "login-name": <value>,
    "login-password": <value>,
    "ssh-private-key": <value>,
    "ssh-unlock": <value>
    "become-mode": <value>,
    "become-user": <value>,
    "become-password": <value>,
    "use-ssh-keys": <value>,
    "comment": <value>
}
```

| Property        | Description of Values                                        |
| --------------- | ------------------------------------------------------------ |
| id              | A UUID for the Machine Credential.                           |
| name            | A human-readable name for the credential. Required.          |
| login-name      | The username that will be used to log in to target nodes over SSH. Required. |
| login-password  | The password that will be used to log in to target nodes over SSH, if using password authentication. |
| ssh-private-key | The private-key that will be used to log in to target nodes over SSH, if using key-based authentication. Must be in OpenSSH format, which is commonly used when creating keys using the OpenSSH ssh-keygen tool. |
| ssh-unlock      | The ssh passphrase required to unlock the key, if the private key requires one. |
| become-mode     | The privilege-escalation mechanism to obtain super-user privileges on target nodes. Can be sudo, su, or direct (if login-name already has super-user privs). Defaults to direct. |
| become-user     | The name of the super-user on target nodes whose privileges will be assumed. Required if become-mode is sudo or su. Defaults to root. |
| become-password | The password that will be used in response to sudo or su prompts on target nodes. Required if the become-mode is sudo or su and the target node prompts for passwords. |
| use-ssh-keys    | Ignored. Optional.                                           |
| comment         | A comment that describes the credential. Optional.           |

## Examples

### Create credentials with private key

```json
{
	"become-mode":"sudo",
	"use-ssh-keys": true,
	"name":"DSE creds",
	"login-user": "<username>",
	"ssh-private-key": "<the path to private key>",
    "become-user": null
}
```

### Create credentials with password

```json
{
	"become-mode": "sudo",
	"use-ssh-keys": false,
    "name": "DSE creds",
	"login-user": "<username>",
	"login-password": "<password>",
	"become-user": null
}
```

