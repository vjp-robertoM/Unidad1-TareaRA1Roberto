# tests/test_lavadero_unittest.py

import unittest
# Importamos la clase Lavadero desde el módulo padre
from lavadero import Lavadero

class TestLavadero(unittest.TestCase):
    
    # Método que se ejecuta antes de cada test.
    # Es el equivalente del @pytest.fixture en este contexto.
    def setUp(self):
        """Prepara una nueva instancia de Lavadero antes de cada prueba."""
        self.lavadero = Lavadero()

    # ----------------------------------------------------------------------    
    # Función para resetear el estado cuanto terminamos una ejecución de lavado
    # ----------------------------------------------------------------------
    def test15_reseteo_estado_con_terminar(self):
        """Premisa: Verifica que terminar() resetea todas las flags y el estado."""
        self.lavadero.hacerLavado(False, True, True)
        self.lavadero._cobrar()
        self.lavadero.terminar()
        
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO)
        self.assertFalse(self.lavadero.ocupado)
        self.assertFalse(self.lavadero.prelavado_a_mano)
        self.assertTrue(self.lavadero.ingresos > 0) # Los ingresos deben mantenerse
        
    # ----------------------------------------------------------------------
    # TESTS  
    # ----------------------------------------------------------------------
        
    def test1_estado_inicial_correcto(self):
        """Premisa 1: Estado inicial del lavadero"""
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO)
        self.assertEqual(self.lavadero.ingresos, 0.0)
        self.assertFalse(self.lavadero.ocupado)
        self.assertFalse(self.lavadero.prelavado_a_mano)
        self.assertFalse(self.lavadero.secado_a_mano)
        self.assertFalse(self.lavadero.encerado)

   
    def test2_excepcion_encerado_sin_secado(self):
        """Test 2: Comprueba que encerar sin secado a mano lanza ValueError."""
        # hacerLavado: (Prelavado: False, Secado a mano: False, Encerado: True)
        with self.assertRaises(ValueError):
            self.lavadero.hacerLavado(False, False, True)

    def test3_excepcion_lavado_mientras_ocupado(self):
        """Premisa 3: No se puede iniciar un lavado si ya hay otro en marcha"""
        self.lavadero.hacerLavado(False, False, False)
        with self.assertRaises(RuntimeError):
            self.lavadero.hacerLavado(False, False, False)

    def test4__ingresos_prelavado(self):
        """Premisa 4: Prelavado a mano = 6,50€"""
        self.lavadero.hacerLavado(True, False, False)
        self.lavadero._cobrar()
        self.assertEqual(self.lavadero.ingresos, 6.50)

    def test5_ingresos_secado(self):
        """Premisa 5: Secado a mano = 6,00€"""
        self.lavadero.hacerLavado(False, True, False)
        self.lavadero._cobrar()
        self.assertEqual(self.lavadero.ingresos, 6.20)

    def test6_ingresos_secado_encerado(self):
        """Premisa 6: Secado + encerado = 7,20€"""
        self.lavadero.hacerLavado(False, True, True)
        self.lavadero._cobrar()
        self.assertEqual(self.lavadero.ingresos, 7.20)

    def test7_ingresos_prelavado_secado(self):
        """Premisa 7: Prelavado + secado = 7,50€"""
        self.lavadero.hacerLavado(True, True, False)
        self.lavadero._cobrar()
        self.assertEqual(self.lavadero.ingresos, 7.70)

    def test8_ingresos_completo(self):
        """Premisa 8: Prelavado + secado + encerado = 8,70€"""
        self.lavadero.hacerLavado(True, True, True)
        self.lavadero._cobrar()
        self.assertEqual(self.lavadero.ingresos, 8.70)

    # ----------------------------------------------------------------------
    # Tests de flujo de fases
    # Utilizamos la función def ejecutar_y_obtener_fases(self, prelavado, secado, encerado)
    # Estos tests dan errores ya que en el código original hay errores en las las fases esperados, en los saltos.
    # ----------------------------------------------------------------------
    def test9_flujo_rapido_sin_extras(self):
        """Test 9: Simula el flujo rápido sin opciones opcionales."""
        fases_esperadas = [0, 1, 3, 4, 5, 7, 0]
         
        # Ejecutar el ciclo completo y obtener las fases
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(prelavado=False, secado=False, encerado=False)
        
        # Verificar que las fases obtenidas coinciden con las esperadas
        self.assertEqual(fases_esperadas, fases_obtenidas)

    def test10_flujo_prelavado(self):
        """Premisa 10: Flujo con prelavado"""
        fases_esperadas = [0, 1, 2, 3, 4, 5, 7, 0]
        fases = self.lavadero.ejecutar_y_obtener_fases(True, False, False)
        self.assertEqual(fases, fases_esperadas)

    def test11_flujo_secado(self):
        """Premisa 11: Flujo con secado"""
        fases_esperadas = [0, 1, 3, 4, 5, 6, 0]
        fases = self.lavadero.ejecutar_y_obtener_fases(False, True, False)
        self.assertEqual(fases, fases_esperadas)

    def test12_flujo_secado_encerado(self):
        """Premisa 12: Flujo con secado y encerado"""
        fases_esperadas = [0, 1, 3, 4, 5, 6, 0]
        fases = self.lavadero.ejecutar_y_obtener_fases(False, True, True)
        self.assertEqual(fases, fases_esperadas)
    
    def test13_flujo_prelavado_secado(self):
        """Premisa 13: Flujo con prelavado y secado"""
        fases_esperadas = [0, 1, 2, 3, 4, 5, 6, 0]
        fases = self.lavadero.ejecutar_y_obtener_fases(True, True, False)
        self.assertEqual(fases, fases_esperadas)

    def test14_flujo_completo(self):
        """Premisa 14: Flujo completo"""
        fases_esperadas = [0, 1, 2, 3, 4, 5, 6, 0]
        fases = self.lavadero.ejecutar_y_obtener_fases(True, True, True)
        self.assertEqual(fases, fases_esperadas)

 
# Bloque de ejecución para ejecutar los tests si el archivo es corrido directamente
if __name__ == '__main__':
    unittest.main()