# lightdash-ops

This is a python-based [Lightdash](https://www.lightdash.com/).
It focuses on to operate resources like users' roles and spaces on Lightdash by calling, as [the official CLI](https://docs.lightdash.com/api/v1/), as [The Lightdash CLI \| Documentation \| Lightdash](https://docs.lightdash.com/guides/cli/intro/) enables us to deploy projects and so on.
For instance, we can get members

## Install

```commandline
pip install -U lightdash-ops
```

## Settings

We can configure the API endpoint and so on with environment variables.
We can also take advantage of an `.env` file.
The template is located at [.env.template](.env.template).

```commandline
# .env
LIGHTDASH_BASE_URL=https://localhost:8000
...
```

### How to use

The CLI requires a personal access token to call the Lightdash APIs.
[The official documentation](https://docs.lightdash.com/references/personal_tokens/) describes how to get personal access tokens.

The CLI provides many sub commands.
Please refer to the detailed documentation in [docs/cli.ms](./docs/cli.md).

#### Example
The subsequent command is used to get all members in an organization.

```commandline
$ export LIGHTDASH_API_KEY="YOUR-LIGHTDASH-PERSONAL-ACCESS-TOKEN"
$ lightdash-ops organization get-members
[
  {
    "member_uuid": "ade0aef5-bca8-4cbe-819b-07803390ffb0",
    "email": "lightdash-member@example.com",
    "role": "member"
  },
  {
    "member_uuid": "d7ee948b-26d6-461a-b289-906cc7bb0c73",
    "email": "lightdash-admin@example.com",
    "role": "admin"
  }
]
```
