"""Módulo de modelos de dominio para MeteoCaracas."""
from .Localidad import Localidad
from .Municipio import Municipio
from .ClimaActual import ClimaActual
from .RegistroHistorico import RegistroHistorico
from .Estadisticas import Estadisticas

__all__ = ["Localidad", "Municipio", "ClimaActual", "RegistroHistorico", "Estadisticas"]
