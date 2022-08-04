# Trash Panda Scripts

This is just a collection of custom service check scripts for the [Trash Panda Project](https://github.com/robweber/trash-panda). As Trash Panda utilizes the same basic return values of other programs (like Nagios or Icinga) these could easily be used on those systems as well.

## Install

Clone the repo and install any requirements. Be aware that this will install the requirements to run all of the scripts, if you want to cherry pick you'll have to look at the exact script you want to run.

```

sudo -H pip3 install -r requirements.txt

```

## Usage

To use with Trash Panda there are two options.

### Method 1

Clone this repo in the same parent directory as the main trash-panda repo. You'll end up with a directory structure like this:

```
/
  /trash-panda/
  /trash-panda-scripts/
```

By default Trash Panda will define a template variable `SCRIPTS_PATH` that will point to this location. You can use this variable as a shortcut when [defining services](https://github.com/robweber/trash-panda/blob/main/README.md#services).

### Method 2
Clone the repo wherever you want and use a `jinja_constant` to define where the path to the repo is. This is done in the [global config](https://github.com/robweber/trash-panda/blob/main/README.md#global-configuration) section of the Trash Panda config file.

```
config:
  default_interval: 3
  jinja_constants:
    SCRIPTS_PATH: /path/to/repo/
```

Once started you can use the `SCRIPT_PATH` template variable as a shortcut to the directory when [defining services](https://github.com/robweber/trash-panda/blob/main/README.md#services).

## License

[MIT](https://github.com/robweber/trash-panda-scripts/blob/main/LICENSE)
