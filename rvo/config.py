import os
import ConfigParser
import rvo.utils as utils

def parse_config(conf="~/.rvo.conf"):

    # soon....
    default = {}
    con = dict()
    config = ConfigParser.ConfigParser()

    if not config.read(os.path.expanduser(conf)):
        utils.log_error("Error: your con %s could not be read" % conf)
        exit(1)

    try:
        con["uri"] = config.get("General", "MongoDB")
    except ConfigParser.NoOptionError:
        utils.log_error("Error: Please set a MongoDB Connection URI in %s" % conf)
        exit(1)

    try:
        con["db"] = config.get("General", "DB")
    except ConfigParser.NoOptionError:
        con["db"] = "rvo"

    try:
        con["editor"] = config.get("General", "Editor")
    except ConfigParser.NoOptionError:
        con["editor"] = "vim"

    try:
        con["pager"] = config.get("General", "Pager")
    except ConfigParser.NoOptionError:
        con["pager"] = "less"

    try:
        con["mailfrom"] = config.get("General", "MailFrom")
    except ConfigParser.NoOptionError:
        con["mailfrom"] = "nobody@example.net"

    con["collection"] = "documents"
    con["shortids"] = "cache"
    con["transactions"] = "transactions"
    con["config"] = "config"

    return con

