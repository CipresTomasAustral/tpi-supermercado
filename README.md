# TPI - Procesamiento de Compras Supermercado

Sistema de procesamiento de compras de supermercado con pipeline de CI/CD usando GitHub Actions.

## Descripcion

El sistema lee un archivo CSV con registros de compras de sucursales y genera estadisticas por producto, por sucursal y totales generales. Incluye un algoritmo de ordenamiento burbuja propio para ordenar el archivo si es necesario.

## Estructura del proyecto

```
tpi-supermercado/
├── supermercado.py
├── test_supermercado.py
├── requirements.txt
└── README.md
```

## Formato del archivo CSV

| Campo  | Descripcion              |
|--------|--------------------------|
| PRSUC  | Codigo de sucursal       |
| PRCOD  | Codigo de producto       |
| PRFEC  | Fecha de compra          |
| PRPROV | Proveedor                |
| PRCANT | Cantidad comprada        |
| PRPRE  | Precio unitario          |

## Uso

```bash
python supermercado.py
```

El programa solicita el path del archivo CSV y si ya esta ordenado (Y/N). Si no esta ordenado aplica bubble sort y genera un archivo `_ordenado.csv`.

## Resultados generados

- Por producto: TOTUNI (total unidades), TOTPES (total en pesos)
- Por sucursal: TOTSUC, MYPROD/MYIMPOR (mayor compra), MNPROD/MNIMPOR (menor compra)
- Totales: CANSUC (cantidad sucursales), TOTALIMP (importe total general)

## Instalacion

```bash
pip install -r requirements.txt
```

## Tests

```bash
pytest test_supermercado.py -v
```
