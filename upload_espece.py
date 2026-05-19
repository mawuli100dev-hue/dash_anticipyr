import streamlit as st
import boto3
import zipfile
import io
import os

from core.constants import B2_KEY_ID, B2_APPLICATION_KEY, B2_ENDPOINT, B2_BUCKET

st.set_page_config(
    page_title=f"Admin - ANTICI'PYR",
    page_icon="🌿",
)

s3 = boto3.client(
    "s3",
    endpoint_url=B2_ENDPOINT,
    aws_access_key_id=B2_KEY_ID,
    aws_secret_access_key=B2_APPLICATION_KEY,
)

st.markdown("""
<style>
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


def lister_especes_bucket() -> list[str]:
    response = s3.list_objects_v2(Bucket=B2_BUCKET, Delimiter="/")
    prefixes = response.get("CommonPrefixes", [])
    return sorted([p["Prefix"].rstrip("/") for p in prefixes])


def supprimer_espece(espece: str) -> None:
    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=B2_BUCKET, Prefix=f"{espece}/")
    for page in pages:
        objets = page.get("Contents", [])
        if objets:
            s3.delete_objects(
                Bucket=B2_BUCKET,
                Delete={"Objects": [{"Key": o["Key"]} for o in objets]},
            )


# ---------------------------------------------------------------------------
st.title("Gestion des espèces")

# --- Section 1 : ajout ---
st.subheader("Ajouter des espèces")
st.write("Dépose un ou plusieurs `.zip` (un par espèce).")

uploaded_files = st.file_uploader(
    "Dossiers espèces (.zip)",
    type="zip",
    accept_multiple_files=True,
)

if uploaded_files:
    for uploaded in uploaded_files:
        with zipfile.ZipFile(io.BytesIO(uploaded.read())) as z:
            fichiers = [f for f in z.namelist()
                        if not os.path.basename(f).startswith("._")
                        and "__MACOSX" not in f
                        and not f.endswith("/")]
        nom_espece = fichiers[0].split("/")[0] if fichiers else uploaded.name
        st.write(f"- **{nom_espece}** - {len(fichiers)} fichiers")

    if st.button("Envoyer tout dans le bucket"):
        for uploaded in uploaded_files:
            with zipfile.ZipFile(io.BytesIO(uploaded.getvalue())) as z:
                fichiers = [f for f in z.namelist()
                            if not os.path.basename(f).startswith("._")
                            and "__MACOSX" not in f
                            and not f.endswith("/")]

                nom_espece = fichiers[0].split("/")[0] if fichiers else uploaded.name
                st.write(f"Envoi de **{nom_espece}**...")
                progress = st.progress(0)

                for i, fichier in enumerate(fichiers):
                    with z.open(fichier) as f:
                        s3.upload_fileobj(f, B2_BUCKET, fichier)
                    progress.progress((i + 1) / len(fichiers))

                st.success(f"{nom_espece} - OK")

        st.balloons()
        st.rerun()

st.divider()

# --- Section 2 : liste des espèces ---
st.subheader("Espèces disponibles")

especes = lister_especes_bucket()

if not especes:
    st.info("Aucune espèce dans le bucket pour l'instant.")
else:
    st.caption(f"{len(especes)} espèce(s) dans le bucket")
    for espece in especes:
        col_nom, col_btn = st.columns([8, 2])
        with col_nom:
            st.markdown(f"*{espece}*")
        with col_btn:
            if st.button("Supprimer", key=f"del_{espece}", type="secondary"):
                supprimer_espece(espece)
                st.success(f"{espece} supprimée.")
                st.rerun()
