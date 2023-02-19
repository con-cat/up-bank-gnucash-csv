# Up Bank to GnuCash CSV exporter

A simple CLI to fetch data from the [Up Bank](https://up.com.au/) API and output CSVs for [GnuCash](https://www.gnucash.org/).

## Setup

### API token
1. Get an [Up Bank API token](https://developer.up.com.au/#getting-started)
1. Set the environment variable `UP_TOKEN` to the value of your token. I recommend using [direnv](https://direnv.net/), run `cp example.envrc .envrc` and add the token to the `.envrc` file you created.

### Installing dependencies

```shell
pip install -r requirements.dev.txt
```

Python 3.11.1 is recommended. [pip-tools](https://github.com/jazzband/pip-tools) is used to manage dependencies.

### Running the thing

```shell
python exporter --start 2022-05-01 --end 2022-05-31
```

Run the `exporter` command with the start and end dates you want to create CSVs for in yyyy-mm-dd format.

CSVs are saved in the project root directory.

## Useful links

- [Up Bank API docs](https://developer.up.com.au/)
- [Up Bank API Python wrapper docs](https://jcwillox.github.io/up-bank-api/)
- [GnuCash docs: Importing transactions from files](https://www.gnucash.org/docs/v4/C/gnucash-help/trans-import.html)
