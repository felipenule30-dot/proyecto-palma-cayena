from whitenoise.storage import CompressedManifestStaticFilesStorage


class ResilientStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """Igual que CompressedManifestStaticFilesStorage, pero NO revienta el
    sitio (error 500) si una plantilla referencia un archivo estático que no
    existe en el manifiesto. En ese caso devuelve la ruta sin hash en vez de
    lanzar una excepción, para que la página siga cargando con normalidad.
    """
    manifest_strict = False
