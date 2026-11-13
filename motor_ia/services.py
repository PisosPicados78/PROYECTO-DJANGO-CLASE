from pathlib import Path
import joblib

ML_MODELS_DIR = Path(__file__).resolve().parent / 'ml_models'
RUTA_MODELO = ML_MODELS_DIR / 'modelo_helpdesk.pkl'
RUTA_VECTORIZADOR = ML_MODELS_DIR / 'vectorizador.pkl'

_modelo = None
_vectorizador = None


def _cargar_artefactos():
    global _modelo, _vectorizador
    if _modelo is None or _vectorizador is None:
        if not RUTA_MODELO.exists() or not RUTA_VECTORIZADOR.exists():
            raise FileNotFoundError(
                f"No se encontraron los archivos .pkl en {ML_MODELS_DIR}"
            )
        _modelo = joblib.load(RUTA_MODELO)
        _vectorizador = joblib.load(RUTA_VECTORIZADOR)
    return _modelo, _vectorizador


def predecir_prioridad(texto):
    texto_limpio = (texto or '').strip()
    if not texto_limpio:
        return 'Media'

    try:
        modelo, vectorizador = _cargar_artefactos()
        vector = vectorizador.transform([texto_limpio])
        return str(modelo.predict(vector)[0])
    except Exception as error:
        print(f"[motor_ia] Error al predecir prioridad: {error}")
        return 'Media'
