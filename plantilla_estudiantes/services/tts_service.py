"""
Servicio de Síntesis de Voz (Text-to-Speech - TTS) con Perfil de Estudiante Guía ETITC.
VERSIÓN PLANTILLA PARA ESTUDIANTES.
"""

import base64
import io
import math
import struct
import wave
from typing import Any, Dict
from models.schemas import IntentMatchResult, TTSOutput


class TTSService:
    """Sintetiza la respuesta institucional con la identidad vocal de un estudiante de la ETITC."""

    def __init__(self, perfil_voz_config: Dict[str, Any]) -> None:
        self.nombre_guia: str = perfil_voz_config.get(
            "nombre_guia", "Estudiante Monitor ETITC"
        )
        self.saludo_inicial: str = perfil_voz_config.get(
            "saludo_inicial", "¡Hola! Hablas con el monitor estudiantil de la ETITC."
        )
        self.muletillas: list[str] = perfil_voz_config.get("muletillas_permitidas", [])
        self.velocidad_wpm: int = int(perfil_voz_config.get("velocidad_wpm", 145))
        self.idioma_codigo: str = perfil_voz_config.get("idioma_codigo", "es-CO")

    @staticmethod
    def _generar_wav_sintetico_base64(duracion_seg: float = 0.35, frecuencia_hz: float = 440.0) -> str:
        """
        Helper entregado: Genera un archivo RIFF WAV PCM mono válido en memoria codificado en Base64.
        """
        sample_rate = 8000
        num_samples = max(int(sample_rate * min(duracion_seg, 0.5)), 800)
        buffer = io.BytesIO()

        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)

            frames = bytearray()
            for i in range(num_samples):
                envolvente = math.sin(math.pi * i / num_samples)
                valor = int(12000 * envolvente * math.sin(2.0 * math.pi * frecuencia_hz * i / sample_rate))
                frames.extend(struct.pack("<h", valor))

            wav_file.writeframes(bytes(frames))

        return base64.b64encode(buffer.getvalue()).decode("ascii")

    def sintetizar_respuesta_estudiante(
    self,
    resultado_intencion: IntentMatchResult,
    incluir_saludo: bool = False
) -> TTSOutput:
    fragmentos: list[str] = []

    if incluir_saludo:
        fragmentos.append(self.saludo_inicial)

    if not resultado_intencion.es_fallback and len(self.muletillas) >= 2:
        fragmentos.append(self.muletillas[0])
        fragmentos.append(self.muletillas[1])

    fragmentos.append(resultado_intencion.respuesta_institucional_exacta)

    if not resultado_intencion.es_fallback and len(self.muletillas) >= 3:
        fragmentos.append(self.muletillas[2])

    guion_completo = " ".join(fragmentos)

    num_palabras = len(guion_completo.split())
    duracion_segundos = round(num_palabras / self.velocidad_wpm * 60.0, 2)

    ssml = (
        f'<speak version="1.0" xml:lang="{self.idioma_codigo}">'
        f'<voice name="{self.nombre_guia}">'
        f'<prosody rate="medium">{escape(guion_completo)}</prosody>'
        f'</voice></speak>'
    )

    audio_b64 = self._generar_wav_sintetico_base64(duracion_seg=duracion_segundos)

    return TTSOutput(
        guion_hablado_estudiante=guion_completo,
        ssml_generado=ssml,
        audio_wav_base64=audio_b64,
        duracion_estimada_segundos=duracion_segundos,
        perfil_voz=self.nombre_guia,
    )
