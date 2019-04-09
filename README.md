
# DB Status

Simple Database healthchecker using Click to verify connections
before executing tasks.

## Installation

## Usage
 - `dbstat` - the entry point for the CLI, use `dbstat --help`
 - This CLI requires you to run either command `dbstat set-url` or `dbstat createconf`
   to run. `createconf` will create a `dbstatus.ini` file in your project directory 
   that contains the necessary information to run the CLI and ping a database. 
   `set-url` will create the config file if it doesn't exist, but will also change the
   uri if it has already been set
 - `dbstat check` - Uses the database uri from the previously mentioned config file,
   unless `--uri` or `-u` is specified, and checks if a connection is made. 

## Features
 - In progress :: Psuedo Database pinger to verify database URI's
 - Not Started :: Query Shell similar to psql
 - Not Started :: Execute SQL from file

## TODO
- [ ] Shell for executing SQL commands for any flavor
- [ ] Load file and execute full scripts

