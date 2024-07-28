import os

import firebase_admin
from django.contrib.auth.models import User
from firebase_admin import auth, credentials
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import Firebase

certificate = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN"),
}

cred = credentials.Certificate(certificate)
firebase_admin.initialize_app(cred)


class FirebaseAuthentication(BaseAuthentication):
    """
    The client will send us an ID token, which is used to verify the request. We will
    use Firebase authentication method to verify the token and extract the UID from it.

    https://firebase.google.com/docs/auth/admin/verify-id-tokens#python
    """

    def authenticate(self, request):
        """
        Returns a tuple of `(user, auth)` if the authentication succeeds, or `None` otherwise.

        The `user` will be an instance of User, either retrieved or created if necessary.
        The `auth` will be the UID retrieved from the Firebase JWT.

        The returned values will also set these attributes on the request object when forwarded, i.e.
        it can later be accessed via `request.user` and `request.uid` when forwarded to the Views.
        """
        firebase_token = request.headers.get("Authorization")
        if not firebase_token:
            return None
        try:
            decoded_token = auth.verify_id_token(firebase_token)
            firebase_uid = decoded_token["uid"]

            firebase_user_exists = Firebase.objects.filter(uid=firebase_uid).exists()
            if firebase_user_exists:
                firebase_user = Firebase.objects.get(uid=firebase_uid)
                user = User.objects.get(id=firebase_user.user_id.id)
            else:
                user = User.objects.create(username=firebase_uid)
                Firebase.objects.create(uid=firebase_uid, user_id=user)
            return user, firebase_uid
        except auth.InvalidIdTokenError:
            raise AuthenticationFailed("Token authentication failed")
