import getpass
import hashlib
import requests


class CommonAPI:
    """
    Construct the Aras API handler by obtaining an access token.

    Parameters
    ----------
    base_url : str
        The url where Aras Innovator is hosted.
        e.g. http://innovator.hangar18.io/InnovatorServer
    client_id : str
        OAuth client ID, see Innovator deployment docs to learn what this is
        and where to find it.
    database : str
        Name of the Aras database to connect to.
    username : str
        A boolean specifying whether to recursively get from child folders.
        Will default to False if omimtted.
    password_hash : hashlib._hashlib.HASH or None
        An md5 hash of the user's password. If this is None or the arg is
        omitted, the user will be prompted for the password via getpass.
    """
    def __init__(self, base_url, client_id, database, username,
                 password_hash=None):

        # Validate inputs.
        if not isinstance(base_url, str):
            raise ValueError(
                "The base_url parameter must be string."
            )

        if not isinstance(client_id, str):
            raise ValueError(
                "The client_id parameter must be string."
            )

        if not isinstance(database, str):
            raise ValueError(
                "The database parameter must be string."
            )

        if not isinstance(username, str):
            raise ValueError(
                "The username parameter must be string."
            )

        if (password_hash is not None and
            not isinstance(password_hash, hashlib._hashlib.HASH)):
            raise ValueError(
                "The password_hash parameter must be an md5 hash object. ",
                "e.g. hashlib.md5( 'PASSWORD'.encode() )"
            )

        if password_hash is not None and password_hash.name != "md5":
            raise RuntimeError(
                "Expected md5 hash for password, but a different hashing ",
                "algorithm was used."
            )

        # Interactively get the password if it was not provided.
        if password_hash is None:
            password_hash_str = hashlib.md5(
                getpass.getpass("Password: ").encode()
            ).hexdigest()
        else:
            password_hash_str = password_hash.hexdigest()

        # TODO: get the base_url and verify that it is a valid InnovatorServer
        self._base_url = base_url

        # Perform initial request.
        oauth_query_url = '{0}/OAuthServer/.well-known/openid-configuration'\
            .format(self._base_url)
        oauth_query_response = requests.get(oauth_query_url)
        token_endpoint_url = oauth_query_response.json()['token_endpoint']

        # Prepare authorization request.
        request_body = {
            "grant_type": "password",
            "scope": "Innovator",
            "client_id": client_id,
            "username": username,
            "password": password_hash_str,
            "database": database
        }

        # Perform authorization request.
        token_response = requests.post(
            url=token_endpoint_url,
            data=request_body
        )

        # This access token will be used to perform all other requests.
        self._authorization = token_response.json()["access_token"]

    # Shortcut for _authorization request header
        self._headers_auth = {
            "Authorization": f"Bearer {self._authorization}",
        }
