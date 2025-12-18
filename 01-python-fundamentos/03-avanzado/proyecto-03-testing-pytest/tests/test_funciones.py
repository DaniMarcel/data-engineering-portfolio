"""
Testing con Pytest - Data Engineering
======================================

Suite de tests para funciones comunes de data engineering.
"""

import pytest
import pandas as pd
from datetime import datetime, date

# ========== FUNCIONES A TESTEAR ==========

def validar_email(email: str) -> bool:
    """Valida formato de email."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def calcular_edad(fecha_nacimiento: date) -> int:
    """Calcula edad desde fecha de nacimiento."""
    today = date.today()
    edad = today.year - fecha_nacimiento.year
    if (today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia un DataFrame."""
    df_clean = df.copy()
    # Remover duplicados
    df_clean = df_clean.drop_duplicates()
    # Remover filas con todos nulos
    df_clean = df_clean.dropna(how='all')
    return df_clean


def calcular_descuento(subtotal: float, pct_descuento: float) -> float:
    """Calcula descuento."""
    if pct_descuento < 0 or pct_descuento > 100:
        raise ValueError("Descuento debe estar entre 0 y 100")
    return subtotal * (pct_descuento / 100)


# ========== TESTS ==========

class TestValidacionEmail:
    """Tests para validación de email."""
    
    def test_email_valido(self):
        assert validar_email("usuario@example.com") == True
        assert validar_email("test.user@domain.co.uk") == True
    
    def test_email_invalido(self):
        assert validar_email("invalido") == False
        assert validar_email("@example.com") == False
        assert validar_email("user@") == False
    
    @pytest.mark.parametrize("email,expected", [
        ("valid@email.com", True),
        ("invalid", False),
        ("missing@domain", False),
        ("good.email@test.org", True),
    ])
    def test_emails_parametrizados(self, email, expected):
        assert validar_email(email) == expected


class TestCalculoEdad:
    """Tests para cálculo de edad."""
    
    def test_edad_basica(self):
        fecha_nac = date(1990, 1, 1)
        edad = calcular_edad(fecha_nac)
        assert edad >= 33  # En 2024
    
    def test_edad_hoy(self):
        hoy = date.today()
        assert calcular_edad(hoy) == 0
    
    def test_cumpleanos_futuro(self):
        # Si el cumpleaños aún no pasó este año
        hoy = date.today()
        fecha_nac = date(2000, 12, 31)
        edad = calcular_edad(fecha_nac)
        assert isinstance(edad, int)
        assert edad >= 0


class TestLimpiezaDatos:
    """Tests para limpieza de datos."""
    
    def test_remover_duplicados(self):
        df = pd.DataFrame({
            'a': [1, 1, 2],
            'b': [3, 3, 4]
        })
        df_clean = limpiar_datos(df)
        assert len(df_clean) == 2
    
    def test_remover_filas_nulas(self):
        df = pd.DataFrame({
            'a': [1, None, 3],
            'b': [None, None, 4]
        })
        df_clean = limpiar_datos(df)
        # La fila del medio (todo None) debe removerse
        assert len(df_clean) == 2
    
    def test_conservar_datos_validos(self):
        df = pd.DataFrame({
            'a': [1, 2, 3],
            'b': [4, 5, 6]
        })
        df_clean = limpiar_datos(df)
        assert len(df_clean) == 3
        assert df_clean.equals(df)


class TestCalculoDescuento:
    """Tests para cálculo de descuentos."""
    
    def test_descuento_10_porciento(self):
        assert calcular_descuento(100, 10) == 10.0
    
    def test_descuento_0_porciento(self):
        assert calcular_descuento(100, 0) == 0.0
    
    def test_descuento_100_porciento(self):
        assert calcular_descuento(100, 100) == 100.0
    
    def test_descuento_invalido_negativo(self):
        with pytest.raises(ValueError):
            calcular_descuento(100, -10)
    
    def test_descuento_invalido_mayor_100(self):
        with pytest.raises(ValueError):
            calcular_descuento(100, 150)
    
    @pytest.mark.parametrize("subtotal,pct,expected", [
        (100, 10, 10.0),
        (200, 25, 50.0),
        (50, 20, 10.0),
    ])
    def test_varios_descuentos(self, subtotal, pct, expected):
        assert calcular_descuento(subtotal, pct) == expected


# ========== FIXTURES ==========

@pytest.fixture
def dataframe_ejemplo():
    """Fixture que retorna un DataFrame de ejemplo."""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'nombre': ['Ana', 'Juan', 'María'],
        'edad': [25, 30, 28]
    })


def test_usar_fixture(dataframe_ejemplo):
    """Ejemplo de uso de fixture."""
    assert len(dataframe_ejemplo) == 3
    assert 'nombre' in dataframe_ejemplo.columns


# ========== MAIN ==========

if __name__ == "__main__":
    pytest.main([__file__, '-v'])
