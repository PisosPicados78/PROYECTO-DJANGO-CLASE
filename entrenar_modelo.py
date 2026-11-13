"""
Script para entrenar y exportar un modelo local de Machine Learning
para clasificar la prioridad de tickets de soporte técnico.
"""

import os
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# 1. Dataset simulado con casos típicos de soporte técnico
datos_entrenamiento = [
    # Prioridad: Alta (caídas críticas, servidores, fallas de arranque, emergencias)
    ("pantalla azul de la muerte al encender equipo", "Alta"),
    ("el servidor principal se cayó y nadie puede trabajar", "Alta"),
    ("servidor caído emergencia total", "Alta"),
    ("no enciende el computador principal de gerencia", "Alta"),
    ("posible ataque de ransomware archivos cifrados", "Alta"),
    ("la base de datos de producción está corrupta", "Alta"),
    ("fallo crítico en el sistema de facturación", "Alta"),
    ("humo y olor a quemado en la torre de servidor", "Alta"),
    ("caída general de la red en toda la oficina", "Alta"),
    ("error fatal no arranca el sistema operativo", "Alta"),

    # Prioridad: Media (bloqueos de cuentas, fallas de aplicaciones, lentitud, impresoras)
    ("olvidé mi contraseña de correo institucional", "Media"),
    ("no puedo ingresar a mi cuenta de usuario", "Media"),
    ("la impresora de red no responde", "Media"),
    ("el sistema está muy lento al generar reportes", "Media"),
    ("error al exportar datos a formato excel", "Media"),
    ("no puedo enviar correos desde outlook", "Media"),
    ("bloqueo de clave tras tres intentos fallidos", "Media"),
    ("acceso denegado a la carpeta compartida del área", "Media"),
    ("error al abrir el programa de contabilidad", "Media"),
    ("no se sincronizan mis archivos con la nube", "Media"),

    # Prioridad: Baja (periféricos, dudas, solicitudes de equipo accesorio, estética)
    ("solicito cambio de mouse y teclado", "Baja"),
    ("necesito un mouse pad nuevo", "Baja"),
    ("instalación de navegador secundario o lector de pdf", "Baja"),
    ("solicitud de segundo monitor para trabajar más cómodo", "Baja"),
    ("mantenimiento preventivo y limpieza de polvo del equipo", "Baja"),
    ("consulta sobre cómo usar la función de búsqueda", "Baja"),
    ("cable de red muy corto necesito uno más largo", "Baja"),
    ("cambiar el soporte elevador de la pantalla", "Baja"),
    ("solicito cotización de auriculares para llamadas", "Baja"),
    ("cambio de silla o accesorios de oficina", "Baja"),
]

def entrenar_y_exportar():
    textos = [texto for texto, _ in datos_entrenamiento]
    etiquetas = [etiqueta for _, etiqueta in datos_entrenamiento]

    print("[*] Entrenando vectorizador de texto...")
    vectorizador = CountVectorizer(lowercase=True)
    X = vectorizador.fit_transform(textos)

    print("[*] Entrenando clasificador Naive Bayes (MultinomialNB)...")
    modelo = MultinomialNB()
    modelo.fit(X, etiquetas)

    # Rutas de exportación dentro de la app motor_ia/ml_models
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ml_models_dir = os.path.join(base_dir, "motor_ia", "ml_models")
    os.makedirs(ml_models_dir, exist_ok=True)
    ruta_modelo = os.path.join(ml_models_dir, "modelo_helpdesk.pkl")
    ruta_vectorizador = os.path.join(ml_models_dir, "vectorizador.pkl")

    # Guardar artefactos
    joblib.dump(modelo, ruta_modelo)
    joblib.dump(vectorizador, ruta_vectorizador)

    print(f"[OK] Modelo guardado con éxito en: {ruta_modelo}")
    print(f"[OK] Vectorizador guardado con éxito en: {ruta_vectorizador}")

    # Pruebas rápidas
    casos_prueba = [
        "El servidor de base de datos no responde",
        "Olvidé mi clave de acceso",
        "El mouse no funciona bien, necesito otro"
    ]
    print("\n--- Pruebas de verificación rápida ---")
    for caso in casos_prueba:
        vec = vectorizador.transform([caso])
        pred = modelo.predict(vec)[0]
        print(f"Texto: '{caso}' -> Prioridad predicha: {pred}")

if __name__ == "__main__":
    entrenar_y_exportar()
