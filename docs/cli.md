# `lightdash-ops`

**Usage**:

```console
$ lightdash-ops [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `organization`
* `project`
* `settings`

## `lightdash-ops organization`

**Usage**:

```console
$ lightdash-ops organization [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get-members`: Get members in an organization as JSON
* `get-projects`: Get all projects in an organization
* `grant-role`: Grant a member a role in the organization

### `lightdash-ops organization get-members`

Get members in an organization as JSON

**Usage**:

```console
$ lightdash-ops organization get-members [OPTIONS]
```

**Options**:

* `--role [admin|developer|editor|interactive_viewer|member|viewer]`: project role
* `--help`: Show this message and exit.

### `lightdash-ops organization get-projects`

Get all projects in an organization

**Usage**:

```console
$ lightdash-ops organization get-projects [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `lightdash-ops organization grant-role`

Grant a member a role in the organization

**Usage**:

```console
$ lightdash-ops organization grant-role [OPTIONS]
```

**Options**:

* `--email TEXT`: member email  [required]
* `--role [admin|developer|editor|interactive_viewer|member|viewer]`: project role
* `--help`: Show this message and exit.

## `lightdash-ops project`

**Usage**:

```console
$ lightdash-ops project [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get-members`: Get the members of a project as JSON
* `get-spaces`: Get all spaces in a project as JSON
* `grant-role`
* `revoke-role`
* `revoke-space-access`: Share space access with another user
* `share-space-access`: Share space access with another user

### `lightdash-ops project get-members`

Get the members of a project as JSON

**Usage**:

```console
$ lightdash-ops project get-members [OPTIONS]
```

**Options**:

* `--project-uuid TEXT`: Lightdash project UUID  [required]
* `--help`: Show this message and exit.

### `lightdash-ops project get-spaces`

Get all spaces in a project as JSON

**Usage**:

```console
$ lightdash-ops project get-spaces [OPTIONS]
```

**Options**:

* `--project-uuid TEXT`: Lightdash project UUID  [required]
* `--help`: Show this message and exit.

### `lightdash-ops project grant-role`

**Usage**:

```console
$ lightdash-ops project grant-role [OPTIONS]
```

**Options**:

* `--project-uuid TEXT`: Lightdash project UUID  [required]
* `--role [admin|developer|editor|interactive_viewer|viewer|member]`: project role  [required]
* `--user-email TEXT`: User email
* `--user-uuid TEXT`: User UUID
* `--dry-run / --no-dry-run`: Dry run if true  [default: no-dry-run]
* `--help`: Show this message and exit.

### `lightdash-ops project revoke-role`

**Usage**:

```console
$ lightdash-ops project revoke-role [OPTIONS]
```

**Options**:

* `--project-uuid TEXT`: Lightdash project UUID  [required]
* `--role [admin|developer|editor|interactive_viewer|viewer|member]`: project role  [required]
* `--user-email TEXT`: User email
* `--user-uuid TEXT`: User UUID
* `--dry-run / --no-dry-run`: Dry run if true  [default: no-dry-run]
* `--help`: Show this message and exit.

### `lightdash-ops project revoke-space-access`

Share space access with another user

**Usage**:

```console
$ lightdash-ops project revoke-space-access [OPTIONS]
```

**Options**:

* `--project-uuid TEXT`: Lightdash project UUID  [required]
* `--space-uuid TEXT`: Lightdash space UUID  [required]
* `--user-uuid TEXT`: Lightdash user UUID  [required]
* `--user-email TEXT`: Lightdash user email  [required]
* `--dry-run / --no-dry-run`: Dry run if true  [default: no-dry-run]
* `--help`: Show this message and exit.

### `lightdash-ops project share-space-access`

Share space access with another user

**Usage**:

```console
$ lightdash-ops project share-space-access [OPTIONS]
```

**Options**:

* `--project-uuid TEXT`: Lightdash project UUID  [required]
* `--space-uuid TEXT`: Lightdash space UUID  [required]
* `--user-uuid TEXT`: Lightdash user UUID  [required]
* `--user-email TEXT`: Lightdash user email  [required]
* `--dry-run / --no-dry-run`: Dry run if true  [default: no-dry-run]
* `--help`: Show this message and exit.

## `lightdash-ops settings`

**Usage**:

```console
$ lightdash-ops settings [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get`: Get the manager settings

### `lightdash-ops settings get`

Get the manager settings

NOTE:
    The output format isn't fully compatible with .env file.

**Usage**:

```console
$ lightdash-ops settings get [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
