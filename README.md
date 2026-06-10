# TPI - Supermercado

Hola profe, este es el trabajo integrador.

El sistema procesa un archivo CSV con compras de sucursales y genera estadisticas por producto, por sucursal y totales generales. Tiene un algoritmo de ordenamiento burbuja propio para ordenar el archivo en caso de que no este ordenado.

## Archivos

- `supermercado.py` - logica principal
- `test_supermercado.py` - pruebas unitarias
- `COMPRAS_supermercado.csv` - archivo de datos
- `requirements.txt` - dependencias

## Formato del CSV

- PRSUC: sucursal
- PRCOD: codigo de producto
- PRFEC: fecha de compra
- PRPROV: proveedor
- PRCANT: cantidad comprada
- PRPRE: precio unitario

## Como ejecutar

```bash
pip install -r requirements.txt
python supermercado.py
```

Pide el path del CSV y si el archivo ya esta ordenado (Y/N). Si no esta ordenado genera un archivo nuevo ordenado y trabaja desde ese.

## Tests

```bash
pytest test_supermercado.py -v
```
