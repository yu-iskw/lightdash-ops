# main

    Usage: main [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  dump-help      Recursively dump the help of all commands.
  dump-settings  Dump the settings of the CLI.
  exposures
  organization


## dump-help

    Usage: main dump-help [OPTIONS]

  Recursively dump the help of all commands.

Options:
  --help  Show this message and exit.


## dump-settings

    Usage: main dump-settings [OPTIONS]

  Dump the settings of the CLI.

Options:
  --help  Show this message and exit.


## organization

    Usage: main organization [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  get-members   Get members in an organization as JSON
  get-projects  Get all projects in an organization


### get-projects

    Usage: main organization get-projects [OPTIONS]

  Get all projects in an organization

Options:
  --help  Show this message and exit.


### get-members

    Usage: main organization get-members [OPTIONS]

  Get members in an organization as JSON

Options:
  --role [admin|developer|editor|interactive_viewer|member|viewer]
                                  Project role
  --help                          Show this message and exit.


## exposures

    Usage: main exposures [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate      Get all projects in an organization
  generate-all  Generate dbt Exposures of all Lightdash projects


### generate-all

    Usage: main exposures generate-all [OPTIONS]

  Generate dbt Exposures of all Lightdash projects

Options:
  --exposure_types TEXT  The types of exposures to generate
  --output TEXT          The path to the output directory  [required]
  --project_names TEXT   The names of the projects to generate exposures for
  --overwrite BOOLEAN    Overwrite the output file
  --help                 Show this message and exit.


### generate

    Usage: main exposures generate [OPTIONS]

  Get all projects in an organization

Options:
  --project_uuid TEXT    The uuid of the project to generate exposures for
                         [required]
  --exposure_types TEXT  The types of exposures to generate
  --help                 Show this message and exit.


