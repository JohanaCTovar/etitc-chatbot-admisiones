"""
Servicio de Reconocimiento de Voz a Texto (Speech-to-Text - STT).
VERSIÓN PLANTILLA PARA ESTUDIANTES.
"""

import base64
import re
import unicodedata
from typing import Dict
from models.schemas import AudioConsultationRequest, STTResult


BANCO_AUDIOS_SIMULADOS: Dict[str, str] = {
    "audio_carreras_01": "Hola, ¿qué ingenierías y programas por ciclos propedéuticos ofrecen en la ETITC?",
    "audio_requisitos_02": "Buenas tardes, ¿qué documentos y requisitos del ICFES necesito para inscribirme?",
    "audio_costos_03": "¿Cuánto vale el PIN de inscripción y cómo funciona la matrícula cero o beca?",
    "audio_fechas_04": "¿En qué fechas se abren las inscripciones y cuándo salen los admitidos?",
    "audio_horarios_05": "Yo trabajo en el día, ¿ustedes tienen jornada nocturna y dónde queda la sede?",
    "audio_sena_06": "Soy tecnólogo del SENA, ¿cómo puedo homologar mis materias por transferencia?",
    "audio_fuera_dominio_07": "¿Me puedes dar la receta para preparar un ajiaco santafereño?"
}


class STTService:
    """Servicio modular para transcribir entradas de voz y normalizar texto en español."""

    @staticmethod
    def normalizar_texto(texto: str) -> str:
        """
        Limpia y estandariza una cadena en español para facilitar la búsqueda de intenciones.
        """
        if not texto or not texto.strip():
            return ""
        texto = texto.lower().strip()
        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
        texto = re.sub(r"[^a-z0-9\s]", " ", texto)
        texto = re.sub(r"\s+", " ", texto)
        return texto.strip()

    def transcribir(self, request: AudioConsultationRequest) -> STTResult:
        """
        Procesa la solicitud de audio o texto y devuelve un objeto `STTResult`.
        """
        if request.audio_id_simulado:
            if request.audio_id_simulado not in BANCO_AUDIOS_SIMULADOS:
                raise ValueError(
                    f"Audio simulado no encontrado: {request.audio_id_simulado}"
                )
            texto_crudo = BANCO_AUDIOS_SIMULADOS[request.audio_id_simulado]
            fuente = "audio_id_simulado"
            confianza = 0.98
        elif request.audio_base64:
            try:
                contenido = base64.b64decode(request.audio_base64, validate=True)
            except Exception as exc:
                raise ValueError("El audio_base64 no es válido") from exc
            clave = contenido.decode("utf-8", errors="ignore").strip()
            texto_crudo = BANCO_AUDIOS_SIMULADOS.get(
                clave, BANCO_AUDIOS_SIMULADOS["audio_carreras_01"]
            )
            fuente = "audio_base64"
            confianza = 0.92
        elif request.texto_directo and request.texto_directo.strip():
            texto_crudo = request.texto_directo.strip()
            fuente = "texto_directo"
            confianza = 1.0
        else:
            raise ValueError(
                "Debe enviar audio_id_simulado, audio_base64 o texto_directo"
            )

        texto_normalizado = self.normalizar_texto(texto_crudo)
        if not texto_normalizado:
            raise ValueError("El texto quedó vacío después de normalizar")

        return STTResult(
            texto_original=texto_crudo,
            texto_normalizado=texto_normalizado,
            fuente_reconocimiento=fuente,
            confianza_stt=confianza,
        )