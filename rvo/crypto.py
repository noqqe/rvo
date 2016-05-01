"""
crypto is used for encryption and decryption
the documents.

init_master and get_master are there for an additional
layer (indirection). Your password only encrypts the
master key once.

Every document is later encrypted and decrypted by the master
key that was generated once.
"""
import sys
import nacl.secret
import nacl.utils
import click
from pyblake2 import blake2b
import utils
import rvo.db as db

class crypto(object):
    """ The crypto class for everything rvo needs. """

    def __init__(self,password=False):
        self.collection = db.get_config_collection()
        coll = self.collection

        r = coll.find_one({"masterkey": {"$exists": True}})
        if r is None:
            self.init_master()

        self._masterkey = self.get_master(password)


    def init_master(self):
        """
        Generates the master key to encrypt all documents later
        Will ask for password to initialize and will put into the collection config
        :returns: bool
        """

        # Configuration collection
        coll = self.collection

        # generate random 256 byte to use as plain masterkey
        masterkey = blake2b(digest_size=32)
        masterkey.update(nacl.utils.random(256))
        masterkey = masterkey.digest()

        # ask for password to de/encrypt the masterkey
        key = blake2b(digest_size=32)
        utils.log_info("Encryption has not been initialized yet. Please enter your password.")
        pw = click.prompt("%s Set Password" % utils.query_prefix, type=str, hide_input=True, confirmation_prompt=True)
        key.update(pw.encode("utf-8"))
        key = key.digest()
        utils.log_info("Password set successfully. Dont forget it, otherwise you are fucked.")

        # encrypt masterkey with user password
        box = nacl.secret.SecretBox(key)
        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
        enc = box.encrypt(masterkey, nonce, encoder=nacl.encoding.HexEncoder)

        r = coll.insert({"masterkey": enc})
        return True

    def get_master(self, password):
        """
        Will be triggered everytime the user tries to access an encrypted
        document from the database. Asks for his password, decrypts master key
        and returns the masterkey what will be an attribute from the crypto class
        :returns: str
        """
        # Fetch encrypted masterkey from db
        coll = self.collection
        masterkey = coll.find_one({"masterkey": {"$exists": True}})
        masterkey = masterkey["masterkey"]

        # hash input pw
        key = blake2b(digest_size=32)

        if password is False:
            password = click.prompt("%s Password" % utils.query_prefix, type=str, hide_input=True)

        key.update(password.encode("utf-8"))
        key = key.digest()


        # init box
        box = nacl.secret.SecretBox(key)

        # use password to decrypt masterkey
        try:
            masterkey = box.decrypt(ciphertext=masterkey, encoder=nacl.encoding.HexEncoder)
            return masterkey
        except nacl.exceptions.CryptoError:
            utils.log_error("Invalid Password")
            sys.exit(1)
            return False


    def encrypt_content(self, content):
        """
        Will encrypt the content that is given with the masterkey from crypto class
        :content: str (plaintext)
        :returns: str (encrypted and encoded in hexdigest)
        """

        # init new blake2b keystore
        # and get password as hex
        try:
            key = blake2b(digest_size=32)
            key.update(self._masterkey)
            key = key.digest()
        except TypeError:
            sys.exit(1)
        box = nacl.secret.SecretBox(key)

        # generate a nonce
        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

        try:
            msg = box.encrypt(content, nonce, encoder=nacl.encoding.HexEncoder)
            return msg
        except nacl.exceptions.CryptoError:
            utils.log_error("Invalid Password")
            return False

    def decrypt_content(self, content):
        """
        Will decrypt the content that is given as argument using the
        masterkey from crypto class.
        :content: str (encrypted and encoded in hexdigest)
        :returns: str (plaintext)
        """

        # init new blake2b keystore and hash
        # masterkey
        try:
            key = blake2b(digest_size=32)
            key.update(self._masterkey)
            key = key.digest()
        except TypeError:
            sys.exit(1)

        box = nacl.secret.SecretBox(key)

        content = content.encode("utf-8")

        try:
            plain = box.decrypt(ciphertext=content, encoder=nacl.encoding.HexEncoder)
            return plain
        except nacl.exceptions.CryptoError:
            utils.log_error("Invalid Password")
            return False
