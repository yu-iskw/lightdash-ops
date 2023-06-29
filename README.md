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

```commandline
$ lightdash-ops organization get-members --api-key "${LIGHTDASH_PERSONAL_ACCESS_TOKEN}"
[
  {
    "member_uuid": "ed4b34e3-390a-4456-9188-f8947f8e600a",
    "email": "yu.ishikawa+lightdash-test2@dr-ubie.com",
    "role": "member"
  },
  {
    "member_uuid": "5e2a5183-7a56-4412-8259-10893b0c8fb7",
    "email": "yu.ishikawa+lightdash-test@dr-ubie.com",
    "role": "admin"
  }
]
```
