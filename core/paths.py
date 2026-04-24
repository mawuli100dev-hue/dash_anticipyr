from __future__ import annotations

import boto3
from botocore.exceptions import ClientError

# --- Config B2 ---
from dash_anticipyr.core.constants import B2_KEY_ID, B2_APPLICATION_KEY, B2_ENDPOINT, B2_BUCKET


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=B2_ENDPOINT,
        aws_access_key_id=B2_KEY_ID,
        aws_secret_access_key=B2_APPLICATION_KEY,
    )


def list_species() -> list[str]:
    """
    Retourne la liste des espèces disponibles dans le bucket.
    Chaque espèce est un préfixe (dossier) de premier niveau.
    """
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=B2_BUCKET, Delimiter="/")
    prefixes = response.get("CommonPrefixes", [])
    return [p["Prefix"].rstrip("/") for p in prefixes]


def list_species_files(espece: str) -> list[str]:
    """
    Retourne tous les fichiers d'une espèce dans le bucket.
    """
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=B2_BUCKET, Prefix=f"{espece}/")
    objects = response.get("Contents", [])
    return [o["Key"] for o in objects]


def get_file_url(key: str, expires_in: int = 3600) -> str:
    """
    Génère une URL présignée pour lire un fichier depuis le bucket.
    expires_in : durée de validité en secondes (défaut 1h)
    """
    s3 = get_s3_client()
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": B2_BUCKET, "Key": key},
        ExpiresIn=expires_in,
    )


def download_file(key: str, dest_path: str) -> None:
    """
    Télécharge un fichier du bucket vers un chemin local.
    """
    s3 = get_s3_client()
    s3.download_file(B2_BUCKET, key, dest_path)
