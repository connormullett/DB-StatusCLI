
# DB Status

Simple Database healthchecker using Click to verify connections
before executing tasks.

DbStatus DOES NOT connect to the server, only the database. Accessing
other databases is doable however you can not view them without knowing the URI

Example SQL Scripts are available in the `sqlscripts` directory to mess around with

Currently only works with PostgreSQL, other server compatibility coming soon

# Requires
- Python3 (shady compatibility with Python2)
- Git
- Databases to connect to

# Installation

## Regular Installation
- Package is not hosted on Pypi yet, use developer install
  without a virtual environment to use it globally.
  Package will soon be pip installable

## Developer Install
 - Clone or fork the repository
   `git clone https://github.com/connormullett/DB-StatusCLI.git && cd DB-StatusCLI`
 - create a virtual environment if desired, however CLI will only be available
   while the virtual evironment is activated
 - `pip install -r requirements.txt` 
 - `pip install -e .`  This will install the CLI as an editable package and you
   will be able to use `dbstat` in terminal to start the CLI

## Usage
 - `dbstat` - the entry point for the CLI, use `dbstat --help`
 - This CLI requires you to run either command `dbstat set-url` or `dbstat createconf`
   to run. `createconf` will create a `dbstatus.ini` file that contains the necessary
   information to run the CLI and ping a database. 
 - `set-url` - will create the config file if it doesn't exist, but will also change the
   uri if it has already been set
 - `dbstat check` - Uses the database uri from the previously mentioned config file,
   unless `--uri` or `-u` is specified, and checks if a connection is made. 
 - `dbstat sql-shell` - start shell for executing sql queries. Uses the URI in config
   file or what is specified with `-u`/`--uri`

## TODO
- [x] Health check database (verify connection is made)
- [x] Shell for executing SQL queries
- [ ] Check URI from CLI
- [x] Load file and execute full scripts
- [ ] Change URI in Shell
- [ ] Command History
- [ ] Execute query from CLI without going into shell
- [x] Detailed debugging for health check fails

## Progress
 - In Progress :: More Shell Commands
 - Not Started :: Change URI in shell
 - Not Started :: Command History

