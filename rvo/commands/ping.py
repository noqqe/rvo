import click
import rvo.db as db
import rvo.utils as utils

@click.command(short_help="Verifys the connection to the database",
               help="""
                Verifys the connection to the database
                and checks read/write access
                """)
def ping():
    """
    Verifys the connection to the database
    and checks read/write access
    :docid: string (will be converted to bson object)
    :returns: bool
    """
    utils.log_info("Trying to connect to database...")
    response = db.db_ping()
    if response:
        utils.log_info("Connection SUCCESSFUL")
    else:
        utils.log_error("Connection FAILED")

    response = db.db_verify()
    utils.log_info("Trying to write, read, delete to test_collection...")
    if response:
        utils.log_info("Interactions were SUCCESSFUL")
    else:
        utils.log_error("Interactions FAILED")

    if not response:
        print("")
        utils.log_error("Please check your configuration file")
        utils.log_error("You may have:")
        utils.log_error("* a syntax error")
        utils.log_error("* the connection scheme is wrong")
        utils.log_error("* the mongodb instance is not running")
        utils.log_error("* the mongodb instance is not reachable")
        utils.log_error("* the authentication on mongodb side does not work or is not enabled")
        return False
    else:
        print("")
        utils.log_info("Awesome, you can go ahead and use rvo!")

    return True
