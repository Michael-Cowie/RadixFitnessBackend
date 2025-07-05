import firebase_admin
from configurations.django_config_parser import django_configs
from django.contrib.auth.models import User
from firebase_admin import auth, credentials
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import Firebase

if django_configs.get("Development", "USE_FIREBASE") == "True":
    certificate = {
        "private_key": django_configs.get("Firebase", "FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
        "private_key_id": django_configs.get("Firebase", "FIREBASE_PRIVATE_KEY_ID"),
        "client_id": django_configs.get("Firebase", "FIREBASE_CLIENT_ID"),
        "client_email": django_configs.get("Firebase", "FIREBASE_CLIENT_EMAIL"),
        "type": django_configs.get("Firebase", "FIREBASE_TYPE"),
        "project_id": django_configs.get("Firebase", "FIREBASE_PROJECT_ID"),
        "auth_uri": django_configs.get("Firebase", "FIREBASE_AUTH_URI"),
        "token_uri": django_configs.get("Firebase", "FIREBASE_TOKEN_URI"),
        "auth_provider_x509_cert_url": django_configs.get("Firebase", "FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": django_configs.get("Firebase", "FIREBASE_CLIENT_X509_CERT_URL"),
        "universe_domain": django_configs.get("Firebase", "FIREBASE_UNIVERSE_DOMAIN"),
    }

    cred = credentials.Certificate(certificate)
    firebase_admin.initialize_app(cred)


class FirebaseAuthentication(BaseAuthentication):
    """
    Verifies Firebase JWT tokens and authenticates users using Firebase UID.
    Creates a Django user on first authentication if not already present.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # Allow other authenticators to try

        try:
            decoded_token = auth.verify_id_token(auth_header.removeprefix("Bearer ").strip())
        except auth.ExpiredIdTokenError:
            raise AuthenticationFailed("Token has expired")
        except auth.RevokedIdTokenError:
            raise AuthenticationFailed("Token has been revoked")
        except auth.InvalidIdTokenError:
            raise AuthenticationFailed("Invalid authentication token")
        except Exception as e:
            raise AuthenticationFailed(f"Authentication failed: {str(e)}")

        if firebase_uid := decoded_token.get("uid"):
            firebase_user, _ = Firebase.objects.get_or_create(
                uid=firebase_uid, defaults={"user_id": User.objects.create_user(username=firebase_uid)}
            )

            return firebase_user.user_id, decoded_token
        else:
            raise AuthenticationFailed("Invalid token payload: UID missing")
