""" The default way that Django gets its settings is from the 
    settings.py in the project directory.  This creates a problem
    since that means you are saving your configurations with your 
    source code, which is not a good idea since it contains secrets 
    and passwords.  This solution allows you to save the configuration
    values in a different directory outside of your source code.  If
    the app is being deployed in a Docker container, then the config
    can be mounted into the container as a secret file.
"""
    

import ConfigParser
import os


def config_gen(conf_loc, default_conf_loc):
    """ Generates a Django configuration file based off of an example
        config file from the project source.  It will create a new file
        at conf_loc, or open it if it already exists.  For each
        configuration section and option in default_conf_loc, it will
        check if the section/option exists in the config, and if not,
        it will add the section or option to the config file.  If the 
        option already exists in the config, it will not overwrite it.
        This allows you to generate a config file from defaults, and
        allow each environment (dev, stg, prod) to customize it's own
        configuration
    """

    conf_dir = os.path.dirname(os.path.realpath(conf_loc))
    if not os.path.exists(conf_dir):
        os.makedirs(conf_dir)
    _config = ConfigParser.ConfigParser()
    _config.read(conf_loc)

    _default = ConfigParser.ConfigParser()
    _default.read(default_conf_loc)

    config_modified = False

    for section in _default.sections():
        if not _config.has_section(section):
            _config.add_section(section)
            config_modified = True
        for option in _default.options(section):
            if not _config.has_option(section, option):
                _config.set(section, option, _default.get(section, option))
                config_modified = True

    if config_modified:
        with open(conf_loc, 'w') as fh:
            _config.write(fh)

    return _config