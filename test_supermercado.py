import unittest
from supermercado import (
    bubble_sort,
    calcular_total_importe,
    calcular_total_unidades,
    producto_mayor_compra_sucursal,
    producto_menor_compra_sucursal,
    procesar,
)


def make_registro(suc, cod, fec, prov, cant, pre):
    return {'PRSUC': suc, 'PRCOD': cod, 'PRFEC': fec, 'PRPROV': prov, 'PRCANT': cant, 'PRPRE': pre}


class TestBubbleSort(unittest.TestCase):

    def test_ordena_por_sucursal(self):
        datos = [
            make_registro('SUC02', 'P100', '2025-01-01', 'PROV01', 10, 100.0),
            make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 10, 100.0),
        ]
        resultado = bubble_sort(datos)
        self.assertEqual(resultado[0]['PRSUC'], 'SUC01')
        self.assertEqual(resultado[1]['PRSUC'], 'SUC02')

    def test_ordena_por_producto_dentro_sucursal(self):
        datos = [
            make_registro('SUC01', 'P200', '2025-01-01', 'PROV01', 10, 100.0),
            make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 10, 100.0),
        ]
        resultado = bubble_sort(datos)
        self.assertEqual(resultado[0]['PRCOD'], 'P100')
        self.assertEqual(resultado[1]['PRCOD'], 'P200')

    def test_lista_vacia(self):
        resultado = bubble_sort([])
        self.assertEqual(resultado, [])

    def test_un_elemento(self):
        datos = [make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 5, 50.0)]
        resultado = bubble_sort(datos)
        self.assertEqual(len(resultado), 1)

    def test_ya_ordenado(self):
        datos = [
            make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 10, 100.0),
            make_registro('SUC01', 'P200', '2025-01-01', 'PROV01', 10, 100.0),
            make_registro('SUC02', 'P100', '2025-01-01', 'PROV01', 10, 100.0),
        ]
        resultado = bubble_sort(datos)
        self.assertEqual(resultado[0]['PRSUC'], 'SUC01')
        self.assertEqual(resultado[1]['PRCOD'], 'P200')
        self.assertEqual(resultado[2]['PRSUC'], 'SUC02')

    def test_ordena_multiples_sucursales(self):
        datos = [
            make_registro('SUC03', 'P100', '2025-01-01', 'PROV01', 10, 100.0),
            make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 10, 100.0),
            make_registro('SUC02', 'P100', '2025-01-01', 'PROV01', 10, 100.0),
        ]
        resultado = bubble_sort(datos)
        self.assertEqual(resultado[0]['PRSUC'], 'SUC01')
        self.assertEqual(resultado[1]['PRSUC'], 'SUC02')
        self.assertEqual(resultado[2]['PRSUC'], 'SUC03')


class TestCalculoImporte(unittest.TestCase):

    def test_calculo_basico(self):
        registros = [
            make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 10, 100.0),
            make_registro('SUC01', 'P100', '2025-01-02', 'PROV01', 5, 200.0),
        ]
        self.assertEqual(calcular_total_importe(registros), 2000.0)

    def test_calculo_lista_vacia(self):
        self.assertEqual(calcular_total_importe([]), 0.0)

    def test_calculo_un_registro(self):
        registros = [make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 3, 50.0)]
        self.assertEqual(calcular_total_importe(registros), 150.0)

    def test_calculo_multiples_registros(self):
        registros = [
            make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 2, 100.0),
            make_registro('SUC01', 'P200', '2025-01-01', 'PROV01', 3, 200.0),
            make_registro('SUC02', 'P100', '2025-01-01', 'PROV01', 1, 50.0),
        ]
        self.assertEqual(calcular_total_importe(registros), 850.0)


class TestCalculoUnidades(unittest.TestCase):

    def test_unidades_basico(self):
        registros = [
            make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 10, 100.0),
            make_registro('SUC01', 'P100', '2025-01-02', 'PROV01', 5, 200.0),
        ]
        self.assertEqual(calcular_total_unidades(registros), 15)

    def test_unidades_lista_vacia(self):
        self.assertEqual(calcular_total_unidades([]), 0)


class TestProductoMayorMenor(unittest.TestCase):

    def test_mayor_compra(self):
        registros = [
            make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 10, 500.0),
            make_registro('SUC01', 'P200', '2025-01-01', 'PROV01', 5, 100.0),
        ]
        prod, importe = producto_mayor_compra_sucursal(registros)
        self.assertEqual(prod, 'P100')
        self.assertEqual(importe, 5000.0)

    def test_menor_compra(self):
        registros = [
            make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 10, 500.0),
            make_registro('SUC01', 'P200', '2025-01-01', 'PROV01', 5, 100.0),
        ]
        prod, importe = producto_menor_compra_sucursal(registros)
        self.assertEqual(prod, 'P200')
        self.assertEqual(importe, 500.0)

    def test_lista_vacia_mayor(self):
        prod, importe = producto_mayor_compra_sucursal([])
        self.assertIsNone(prod)
        self.assertEqual(importe, 0.0)

    def test_lista_vacia_menor(self):
        prod, importe = producto_menor_compra_sucursal([])
        self.assertIsNone(prod)
        self.assertEqual(importe, 0.0)

    def test_un_solo_producto(self):
        registros = [make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 4, 250.0)]
        prod_max, imp_max = producto_mayor_compra_sucursal(registros)
        prod_min, imp_min = producto_menor_compra_sucursal(registros)
        self.assertEqual(prod_max, 'P100')
        self.assertEqual(prod_min, 'P100')
        self.assertEqual(imp_max, 1000.0)
        self.assertEqual(imp_min, 1000.0)


class TestProcesar(unittest.TestCase):

    def _datos_dos_sucursales(self):
        return [
            make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 10, 100.0),
            make_registro('SUC01', 'P200', '2025-01-02', 'PROV01', 5, 200.0),
            make_registro('SUC02', 'P100', '2025-01-01', 'PROV01', 20, 50.0),
        ]

    def test_cantidad_sucursales(self):
        _, lineas_suc, _ = procesar(self._datos_dos_sucursales())
        self.assertEqual(len(lineas_suc), 2)

    def test_cansuc_en_totales(self):
        _, _, lineas_total = procesar(self._datos_dos_sucursales())
        self.assertIn('CANSUC: 2', lineas_total[0])

    def test_totalimp_en_totales(self):
        _, _, lineas_total = procesar(self._datos_dos_sucursales())
        self.assertIn('TOTALIMP:', lineas_total[0])

    def test_detalle_producto_contiene_totuni(self):
        lineas_prod, _, _ = procesar(self._datos_dos_sucursales())
        encontrado = any('TOTUNI' in l for l in lineas_prod)
        self.assertTrue(encontrado)

    def test_detalle_producto_contiene_totpes(self):
        lineas_prod, _, _ = procesar(self._datos_dos_sucursales())
        encontrado = any('TOTPES' in l for l in lineas_prod)
        self.assertTrue(encontrado)

    def test_datos_invalidos_cantidad_cero(self):
        registros = [make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 0, 100.0)]
        lineas_prod, _, _ = procesar(registros)
        self.assertIn('TOTUNI: 0', lineas_prod[0])

    def test_datos_invalidos_precio_cero(self):
        registros = [make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 5, 0.0)]
        lineas_prod, _, _ = procesar(registros)
        self.assertIn('TOTPES: 0.00', lineas_prod[0])


if __name__ == '__main__':
    unittest.main()


class TestCalculoImporteAdicional(unittest.TestCase):

    def test_precio_decimal(self):
        registros = [make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 4, 12.50)]
        self.assertEqual(calcular_total_importe(registros), 50.0)

    def test_unidades_acumuladas(self):
        registros = [
            make_registro('SUC01', 'P100', '2025-01-01', 'PROV01', 100, 10.0),
            make_registro('SUC01', 'P100', '2025-01-02', 'PROV01', 200, 10.0),
        ]
        self.assertEqual(calcular_total_unidades(registros), 300)
