# Repository

Repositories contain the Debian or RPM packages that LCM uses to install DSE. DataStax public repos can be used, or you can setup your own package repositories.

| [Managing Repositories](https://docs.datastax.com/en/opscenter/6.7/api/docs/lcm_repository.html#managing-repositories) | URL                                                          |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Get a repository object by ID                                | [`GET /api/v2/lcm/repositories/{id}`](https://docs.datastax.com/en/opscenter/6.7/api/docs/lcm_repository.html#method-get-repository-object) |
| Get a list of repositories                                   | [`GET /api/v2/lcm/repositories/`](https://docs.datastax.com/en/opscenter/6.7/api/docs/lcm_repository.html#method-get-repository-list) |
| Create a repository                                          | [`POST /api/v2/lcm/repositories/`](https://docs.datastax.com/en/opscenter/6.7/api/docs/lcm_repository.html#method-post-repository-object) |
| Update a repository                                          | [`PUT /api/v2/lcm/repositories/{id}`](https://docs.datastax.com/en/opscenter/6.7/api/docs/lcm_repository.html#method-put-repository-object) |
| Delete a repository                                          | [`DELETE /api/v2/lcm/repositories/{id}`](https://docs.datastax.com/en/opscenter/6.7/api/docs/lcm_repository.html#method-delete-repository-object) |

## Managing Repositories

### Repository

```json
{     
    "id": "<value>",
    "name": "<value>",
    "repo-key-url": "<value>",
    "repo-url": "<value>",
    "username": "<value>",
    "password": "<value>",
    "use-proxy": "<value>",
    "deb-dist": "<value>",
    "deb-components": "<value>",
    "manual-repository-setup": "<value>",
    "comment": "<value>
} 
```

| Property                | Description of Values                                        |
| ----------------------- | ------------------------------------------------------------ |
| id                      | A UUID for the Repository.                                   |
| name                    | A user-defined name for the Repository. Required.            |
| repo-key-url            | The URL to the repository key for verifying package signatures. Defaults to DataStax repo if null. |
| repo-url                | The URL to the package repository. Defaults to DataStax repo if null. |
| username                | The username for basic auth credentials (if required by the repo). |
| password                | The password for basic auth credentials.                     |
| use-proxy               | A boolean flag indicating whether to use the http proxy (set in the [Config Profile](https://docs.datastax.com/en/opscenter/6.7/api/docs/lcm_config_profile.html#lcm-config-profile)). |
| deb-dist                | Specifies the Debian distribution part of the Apt configuration line. Defaults to ‘stable’. For Apt repositories only. |
| deb-components          | A comma-separated string of the Debian components part of the Apt configuration line. Defaults to ‘main’. |
| manual-repository-setup | If set to true, LCM does not attempt to add any repositories to the target nodes.  The only fields that are used if this value is true are id, name, and comment. |
| comment                 | A generic field for user comments.                           |

