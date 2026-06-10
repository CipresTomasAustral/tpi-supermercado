import csv
import os


def bubble_sort(registros):  # complejidad O(n^2)
    n = len(registros)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            a = registros[j]
            b = registros[j + 1]
            if (a['PRSUC'], a['PRCOD'], a['PRFEC'], a['PRPROV']) > \
               (b['PRSUC'], b['PRCOD'], b['PRFEC'], b['PRPROV']):
                registros[j], registros[j + 1] = registros[j + 1], registros[j]
    return registros


def leer_csv(path):
    registros = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row['PRSUC'] or not row['PRCOD']:
                continue
            registros.append({
                'PRSUC': row['PRSUC'],
                'PRCOD': row['PRCOD'],
                'PRFEC': row['PRFEC'],
                'PRPROV': row['PRPROV'],
                'PRCANT': int(row['PRCANT']),
                'PRPRE': float(row['PRPRE'])
            })
    return registros


def escribir_csv(registros, path):
    campos = ['PRSUC', 'PRCOD', 'PRFEC', 'PRPROV', 'PRCANT', 'PRPRE']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(registros)


def calcular_total_importe(registros):
    total = 0.0
    for r in registros:
        total += r['PRCANT'] * r['PRPRE']
    return round(total, 2)


def calcular_total_unidades(registros):
    total = 0
    for r in registros:
        total += r['PRCANT']
    return total


def producto_mayor_compra_sucursal(registros_sucursal):
    totales = {}
    for r in registros_sucursal:
        cod = r['PRCOD']
        importe = r['PRCANT'] * r['PRPRE']
        totales[cod] = totales.get(cod, 0.0) + importe
    if not totales:
        return None, 0.0
    max_prod = max(totales, key=lambda k: totales[k])
    return max_prod, round(totales[max_prod], 2)


def producto_menor_compra_sucursal(registros_sucursal):
    totales = {}
    for r in registros_sucursal:
        cod = r['PRCOD']
        importe = r['PRCANT'] * r['PRPRE']
        totales[cod] = totales.get(cod, 0.0) + importe
    if not totales:
        return None, 0.0
    min_prod = min(totales, key=lambda k: totales[k])
    return min_prod, round(totales[min_prod], 2)


def procesar(registros):
    sucursal_actual = None
    producto_actual = None

    totuni_prod = 0
    totpes_prod = 0.0

    totsuc = 0
    prod_importes_suc = {}

    cansuc = 0
    totalimp = 0.0

    lineas_producto = []
    lineas_sucursal = []
    lineas_total = []

    for r in registros:
        suc = r['PRSUC']
        prod = r['PRCOD']
        cant = r['PRCANT']
        importe = cant * r['PRPRE']

        if suc != sucursal_actual:
            if producto_actual is not None:
                lineas_producto.append(
                    f"  Producto: {producto_actual} | TOTUNI: {totuni_prod} | TOTPES: {totpes_prod:.2f}"
                )
                prod_importes_suc[producto_actual] = prod_importes_suc.get(producto_actual, 0.0) + totpes_prod

            if sucursal_actual is not None:
                myprod, myimpor = producto_mayor_compra_sucursal(
                    [r2 for r2 in registros if r2['PRSUC'] == sucursal_actual]
                )
                mnprod, mnimpor = producto_menor_compra_sucursal(
                    [r2 for r2 in registros if r2['PRSUC'] == sucursal_actual]
                )
                lineas_sucursal.append(
                    f"Sucursal: {sucursal_actual} | TOTSUC: {totsuc} | "
                    f"MYPROD: {myprod} MYIMPOR: {myimpor:.2f} | "
                    f"MNPROD: {mnprod} MNIMPOR: {mnimpor:.2f}"
                )
                totalimp += sum(prod_importes_suc.values())
                cansuc += 1

            sucursal_actual = suc
            producto_actual = prod
            totuni_prod = 0
            totpes_prod = 0.0
            totsuc = 0
            prod_importes_suc = {}

        elif prod != producto_actual:
            lineas_producto.append(
                f"  Producto: {producto_actual} | TOTUNI: {totuni_prod} | TOTPES: {totpes_prod:.2f}"
            )
            prod_importes_suc[producto_actual] = prod_importes_suc.get(producto_actual, 0.0) + totpes_prod
            producto_actual = prod
            totuni_prod = 0
            totpes_prod = 0.0

        totuni_prod += cant
        totpes_prod += importe
        totsuc += cant

    if producto_actual is not None:
        lineas_producto.append(
            f"  Producto: {producto_actual} | TOTUNI: {totuni_prod} | TOTPES: {totpes_prod:.2f}"
        )
        prod_importes_suc[producto_actual] = prod_importes_suc.get(producto_actual, 0.0) + totpes_prod

    if sucursal_actual is not None:
        myprod, myimpor = producto_mayor_compra_sucursal(
            [r2 for r2 in registros if r2['PRSUC'] == sucursal_actual]
        )
        mnprod, mnimpor = producto_menor_compra_sucursal(
            [r2 for r2 in registros if r2['PRSUC'] == sucursal_actual]
        )
        lineas_sucursal.append(
            f"Sucursal: {sucursal_actual} | TOTSUC: {totsuc} | "
            f"MYPROD: {myprod} MYIMPOR: {myimpor:.2f} | "
            f"MNPROD: {mnprod} MNIMPOR: {mnimpor:.2f}"
        )
        totalimp += sum(prod_importes_suc.values())
        cansuc += 1

    lineas_total.append(f"CANSUC: {cansuc} | TOTALIMP: {totalimp:.2f}")

    return lineas_producto, lineas_sucursal, lineas_total


def imprimir_resultados(lineas_producto, lineas_sucursal, lineas_total):
    print("=" * 60)
    print("DETALLE POR PRODUCTO")
    print("=" * 60)
    for l in lineas_producto:
        print(l)
    print()
    print("=" * 60)
    print("DETALLE POR SUCURSAL")
    print("=" * 60)
    for l in lineas_sucursal:
        print(l)
    print()
    print("=" * 60)
    print("TOTALES GENERALES")
    print("=" * 60)
    for l in lineas_total:
        print(l)


def main():
    path_csv = input("Indique el path del csv: ").strip()

    if not path_csv:
        print("Error: debe ingresar un path valido.")
        return
    if not os.path.exists(path_csv):
        print(f"Error: el archivo '{path_csv}' no existe.")
        return

    ordenado = input("El archivo esta ordenado? (Y/N): ").strip().upper()

    if ordenado == 'N':
        print("Ordenando archivo con bubble sort...")
        registros = leer_csv(path_csv)
        registros = bubble_sort(registros)
        path_ordenado = path_csv.replace('.csv', '_ordenado.csv')
        escribir_csv(registros, path_ordenado)
        print(f"Archivo ordenado guardado en: {path_ordenado}")
        path_csv = path_ordenado
    elif ordenado == 'Y':
        registros = leer_csv(path_csv)
    else:
        print("Opcion invalida. Debe ingresar Y para ordenado o N para desordenado.")
        return

    lineas_producto, lineas_sucursal, lineas_total = procesar(registros)
    imprimir_resultados(lineas_producto, lineas_sucursal, lineas_total)


if __name__ == '__main__':
    main()
