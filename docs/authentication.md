<div align="center">
    <h1> Authentication </h1>
</div>


This project uses **Firebase Authentication** as the primary method for identifying users. A custom DRF authentication class named `FirebaseAuthentication` is used to handle Firebase JWT (ID tokens) verification and user session creation.

## 1. Token Submission

Clients must send a valid **Firebase ID token (JWT)** with each request, using `Authorization` header.

```HTTP
Authorization: Bearer <Firebase_ID_Token>
```

## 2. Token Verification

The `FirebaseAuthentication` class, which is defined as a `BaseAuthentication` subclass handles authentication by verifying the token using Firebase Admin SDK.

```python
decoded_token = auth.verify_id_token(...)
```


```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "firebase.auth.FirebaseAuthentication"
    ],
    ...
```

The `DEFAULT_AUTHENTICATION_CLASSES` ensures that every request passes through the `FirebaseAuthentication` class. Authentication is handled **before** the request reaches any API view — no manual authentication is needed in views.

## 3. User Resolution

After extracting the Firebase UID,

- If the UID is linked to an existing record in the `Firebase` table, the associated `User` is retrieved.
- If the UID is not found, a new `User` is created and a new `Firebase` model entry is stored.

## 4. Authentication Outcome

- If successful, DRF sets `request.user` to the resolved Django `User`
- Additionally, `request.uid` is set to the Firebase UID for downstream use.
- If authentication fails, a `401 Unauthorized` response is returned.
 