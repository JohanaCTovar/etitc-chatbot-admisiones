"""
Motor Determinista de Intenciones Institucionales (Cero Alucinaciones).
VERSIÓN PLANTILLA PARA ESTUDIANTES.
"""

import json
from pathlib import Path
from typing import Any, Dict, List
from models.schemas import IntentMatchResult
from services.stt_service import STTService


class IntentService:
    """Gestiona la carga de la base de conocimiento y la búsqueda determinista de intenciones."""

    def __init__(self, json_path: Path | None = None) -> None:
        if json_path is None:
            json_path = Path(__file__).resolve().parent.parent / "data" / "faqs_admisiones_etitc.json"
        self.json_path = json_path
        self.kb_data: Dict[str, Any] = self._cargar_base_conocimiento()

    def _cargar_base_conocimiento(self) -> Dict[str, Any]:
        """Lee el archivo JSON con las preguntas frecuentes oficiales de la ETITC."""
        if not self.json_path.exists():
            raise FileNotFoundError(f"No se encontró la base de conocimiento en: {self.json_path}")

        with open(self.json_path, mode="r", encoding="utf-8") as file:
            return json.load(file)

    def obtener_catalogo_intenciones(self) -> List[Dict[str, Any]]:
        """Retorna el listado resumido de intenciones soportadas para consulta pública."""
        return [
            {
                "intent_id": item["intent_id"],
                "categoria": item["categoria"],
                "preguntas_ejemplo": item.get("preguntas_ejemplo", []),
                "keywords": item.get("keywords", [])
            }
            for item in self.kb_data.get("intenciones", [])
        ]

    def resolver_intencion(self, texto_normalizado: str) -> IntentMatchResult:
        """
        Busca la intención institucional que mejor coincide con `texto_normalizado`
        sin inventar ni modificar ninguna respuesta oficial.
        """
        # TODO: [Estudiante 3] - Programar el motor determinista de clasificación de intenciones.
        # Pasos que debes programar aquí:
        # 1. Separar `texto_normalizado` en un conjunto de palabras (`tokens_consulta = set(texto_normalizado.split())`).
        # 2. Recorrer cada diccionario de intención dentro de `self.kb_data.get("intenciones", [])`.
        # 3. Para cada palabra clave (`kw`) de la intención:
        #    - Normalizar la palabra clave con `STTService.normalizar_texto(kw)`.
        #    - Si la palabra clave tiene espacios (frase compuesta), comprobar si está contenida en `texto_normalizado`.
        #    - Si es una sola palabra, comprobar si pertenece al conjunto `tokens_consulta`.
        #    - Guardar las keywords que coincidieron en una lista.
        # 4. Calcular un puntaje de coincidencia entre 0.0 y 1.0 (por ejemplo, `min(0.35 + len(coincidencias) * 0.22, 0.99)`)
        #    y conservar la intención que obtenga el mayor puntaje.
        # 5. REGLA ANTI-ALUCINACIONES:
        #    - Si ninguna intención tuvo keywords coincidentes, tomar `self.kb_data["respuesta_fallback"]`
        #      y retornar un `IntentMatchResult` con `es_fallback=True`, `puntaje_coincidencia=0.0`
        #      y la `respuesta_oficial` del bloque fallback.
        #    - Si hubo coincidencia, retornar `IntentMatchResult` con los datos exactos de la intención ganadora
        #      y `es_fallback=False`.
        raise NotImplementedError(
            "TODO: [Estudiante 3] Debe implementar IntentService.resolver_intencion()"
        )
