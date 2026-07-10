def validar_descuento(valor_desc):
    """Valida si el descuento está estrictamente entre 1 y 80 (IL 4.1.8)."""
    return 1.0 <= valor_desc <= 80.0

def validar_crecimiento(valor_crec):
    """Valida si el crecimiento está estrictamente entre 1 y 500 (IL 4.1.8)."""
    return 1.0 <= valor_crec <= 500.0

def buscar_juego_en_inventario(id_juego, inv_dict):
    
    if id_juego in inv_dict:
        return inv_dict[id_juego]
    return None

def ordenar_por_llave_descendente(lista, llave):
    n = len(lista)
    for i in range(n):
        for j in range(0, n-i-1):
            if lista[j][llave] < lista[j+1][llave]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista

def ordenar_recomendaciones_avanzado(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n-i-1):
            cambiar = False
            if lista[j]["puntaje"] < lista[j+1]["puntaje"]:
                cambiar = True
            elif lista[j]["puntaje"] == lista[j+1]["puntaje"]:
                if lista[j]["stock"] < lista[j+1]["stock"]:
                    cambiar = True
                elif lista[j]["stock"] == lista[j+1]["stock"]:
                    if lista[j]["precio"] > lista[j+1]["precio"]: # Menor precio va primero
                        cambiar = True
                    elif lista[j]["precio"] == lista[j+1]["precio"]:
                        if lista[j]["titulo"] > lista[j+1]["titulo"]: # Orden alfabético
                            cambiar = True
            if cambiar:
                lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista

def mostrar_menu():
    """SOLO imprime las opciones del menú en pantalla (IL 4.1.1)."""
    print("\n=======================================================")
    print("      SISTEMA DE INTELIGENCIA COMERCIAL (SICV)         ")
    print("=======================================================")
    print("1. Requerimiento 1: Índice de Riesgo Operacional")
    print("2. Requerimiento 2: Índice de Rentabilidad Ponderada")
    print("3. Requerimiento 3: Detección de Anomalías (Auditoría)")
    print("4. Requerimiento 4: Proyección Comercial")
    print("5. Requerimiento 5: Índice Estratégico por Plataforma")
    print("6. Requerimiento 6: Motor de Recomendación")
    print("7. Requerimiento 7: Simulación de Expansión Internacional")
    print("8. Salir del Sistema")
    print("=======================================================")

def leer_opcion():
    """SOLO lee la opción, maneja excepciones numéricas y valida rangos (IL 4.1.2)."""
    try:
        opc = int(input("Seleccione una opción (1-8): "))
        if 1 <= opc <= 8:
            return opc
        else:
            print("Error: Opción fuera de rango (1-8).")
            return -1
    except ValueError:
        print("Error: Debe ingresar un número entero válido.")
        return -1

def ejecutar_requerimiento_1(juegos_dict, inv_dict):
    print("\n--- REQUERIMIENTO 1: ÍNDICE DE RIESGO OPERACIONAL ---")
    total_stock, cont_stock, total_precio, cont_precio = 0, 0, 0.0, 0
    conteo_plataformas = {}
    
    for id_juego, datos in juegos_dict.items():
        total_precio += float(datos["precio"]) 
        cont_precio += 1
        plat = datos["plataforma"]
        conteo_plataformas[plat] = conteo_plataformas.get(plat, 0) + 1
        
        registro_inv = buscar_juego_en_inventario(id_juego, inv_dict)
        if registro_inv is not None:
            total_stock += int(registro_inv["stock_actual"])
            cont_stock += 1
            
    if cont_precio == 0 or cont_stock == 0:
        print("Error: Catálogo sin registros suficientes.")
        return

    prom_precio = total_precio / cont_precio
    prom_stock = total_stock / cont_stock
    
    plat_mayor = ""
    max_juegos_plat = -1
    for plat, cant in conteo_plataformas.items():
        if cant > max_juegos_plat:
            max_juegos_plat = cant
            plat_mayor = plat
            
    juegos_riesgo = []
    for id_juego, datos in juegos_dict.items():
        registro_inv = buscar_juego_en_inventario(id_juego, inv_dict)
        if registro_inv is not None:
            stock = int(registro_inv["stock_actual"])
            if (stock < prom_stock and 
                float(datos["precio"]) > prom_precio and 
                datos["clasificacion"] in ["T", "M"] and 
                datos["plataforma"] != plat_mayor):
                
                juegos_riesgo.append({
                    "titulo": datos["titulo"],
                    "precio": float(datos["precio"]),
                    "plataforma": datos["plataforma"]
                })
                
    juegos_riesgo = ordenar_por_llave_descendente(juegos_riesgo, "precio")
    
    print(f"Plataforma con más juegos (excluida): {plat_mayor}")
    print(f"Precio Promedio: ${prom_precio:.2f} | Stock Promedio: {prom_stock:.2f}")
    print("\nRanking de Juegos en Riesgo:")
    for j in juegos_riesgo:
        print(f"- {j['titulo']} ({j['plataforma']}): ${j['precio']:.2f}")
        
    porcentaje = (len(juegos_riesgo) / cont_precio) * 100
    print(f"\nRepresentan el {porcentaje:.2f}% del catálogo total.")


def ejecutar_requerimiento_2(juegos_dict, inv_dict):
    print("\n--- REQUERIMIENTO 2: ÍNDICE DE RENTABILIDAD PONDERADA ---")
    juego_mayor, juego_menor = None, None
    max_irp, min_irp, suma_irp = -1.0, float('inf'), 0.0
    lista_irp = []
    
    for id_juego, datos in juegos_dict.items():
        registro_inv = buscar_juego_en_inventario(id_juego, inv_dict)
        if registro_inv is not None:
            stock = int(registro_inv["stock_actual"])
            
            factor_clasi = 1.0
            if datos["clasificacion"] == "T": factor_clasi = 1.15
            elif datos["clasificacion"] == "M": factor_clasi = 1.30
            
            factor_multi = 1.20 if datos["multiplayer"] else 1.00
            
            irp = (float(datos["precio"]) * stock) * factor_clasi * factor_multi
            suma_irp += irp
            lista_irp.append(irp)
            
            if irp > max_irp:
                max_irp = irp
                juego_mayor = datos["titulo"]
            if irp < min_irp:
                min_irp = irp
                juego_menor = datos["titulo"]
                
    if not lista_irp:
        print("No se encontraron relaciones válidas de inventario.")
        return
        
    prom_irp = suma_irp / len(lista_irp)
    superan_prom = 0
    for val in lista_irp:
        if val > prom_irp:
            superan_prom += 1
            
    print(f"Juego con Mayor IRP: {juego_mayor} (${max_irp:,.2f})")
    print(f"Juego con Menor IRP: {juego_menor} (${min_irp:,.2f})")
    print(f"IRP Promedio: ${prom_irp:,.2f}")
    print(f"Juegos que superan el promedio: {superan_prom}")


def ejecutar_requerimiento_3(juegos_dict, inv_dict):
    print("\n--- REQUERIMIENTO 3: DETECCIÓN DE ANOMALÍAS ---")
    
    tipo_A = 0
    for id_juego in juegos_dict:
        if buscar_juego_en_inventario(id_juego, inv_dict) is None:
            tipo_A += 1
            
    tipo_B = 0
    for id_inv in inv_dict:
        if id_inv not in juegos_dict:
            tipo_B += 1
            
    tipo_C, tipo_D = 0, 0
    vistos_cd = []
    
    for id1, j1 in juegos_dict.items():
        for id2, j2 in juegos_dict.items():
            if id1 < id2:
                if j1["titulo"] == j2["titulo"] and j1["plataforma"] != j2["plataforma"]:
                    combo = tuple(sorted([id1, id2]))
                    if combo not in vistos_cd:
                        tipo_C += 1
                if j1["titulo"] == j2["titulo"] and j1["editor"] == j2["editor"] and j1["genero"] == j2["genero"]:
                    tipo_D += 1

    tipo_E = 0
    precios_por_plat = {}
    for j in juegos_dict.values():
        plat = j["plataforma"]
        if plat not in precios_por_plat:
            precios_por_plat[plat] = {"suma": 0.0, "cant": 0}
        precios_por_plat[plat]["suma"] += float(j["precio"])
        precios_por_plat[plat]["cant"] += 1
        
    for j in juegos_dict.values():
        plat = j["plataforma"]
        prom_plat = precios_por_plat[plat]["suma"] / precios_por_plat[plat]["cant"]
        if float(j["precio"]) > (prom_plat * 4.0): 
            tipo_E += 1
            
    print("AUDITORÍA FINALIZADA")
    print(f"Tipo A: {tipo_A} registros")
    print(f"Tipo B: {tipo_B} registros")
    print(f"Tipo C: {tipo_C} registros")
    print(f"Tipo D: {tipo_D} registros")
    print(f"Tipo E: {tipo_E} registros")


def ejecutar_requerimiento_4(juegos_dict, inv_dict):
    print("\n--- REQUERIMIENTO 4: PROYECCIÓN COMERCIAL ---")
    
    try:
        desc_input = float(input("Ingrese porcentaje de descuento (1 a 80): "))
        crec_input = float(input("Ingrese porcentaje de crecimiento esperado en ventas (1 a 500): "))
    except ValueError:
        print("Error: Los porcentajes ingresados deben ser valores numéricos decimales.")
        return

    if not validar_descuento(desc_input) or not validar_crecimiento(crec_input):
        print("Error: Uno o ambos valores están fuera de los rangos estipulados.")
        return

    ingreso_total = 0.0
    ingresos_por_plat, ingresos_por_editor = {}, {}
    lista_juegos_proyeccion = []
    
    for id_juego, datos in juegos_dict.items():
        registro_inv = buscar_juego_en_inventario(id_juego, inv_dict)
        if registro_inv is not None:
            stock_actual = int(registro_inv["stock_actual"])
            
            precio_desc = float(datos["precio"]) * (1.0 - (desc_input / 100.0))
            stock_proy = stock_actual + (stock_actual * (crec_input / 100.0))
            ingreso_esperado = precio_desc * stock_proy
            
            ingreso_total += ingreso_esperado
            
            plat = datos["plataforma"]
            ingresos_por_plat[plat] = ingresos_por_plat.get(plat, 0.0) + ingreso_esperado
            
            edit = datos["editor"]
            ingresos_por_editor[edit] = ingresos_por_editor.get(edit, 0.0) + ingreso_esperado
            
            lista_juegos_proyeccion.append({"titulo": datos["titulo"], "ingreso": ingreso_esperado})
            
    max_plat, max_val_plat = "", -1.0
    for p, v in ingresos_por_plat.items():
        if v > max_val_plat:
            max_val_plat = v
            max_plat = p
            
    max_edit, max_val_edit = "", -1.0
    for e, v in ingresos_por_editor.items():
        if v > max_val_edit:
            max_val_edit = v
            max_edit = e
            
    lista_juegos_proyeccion = ordenar_por_llave_descendente(lista_juegos_proyeccion, "ingreso")
    
    print(f"\nIngreso Esperado Total: ${ingreso_total:,.2f}")
    print(f"Plataforma con mayor ingreso esperado: {max_plat} (${max_val_plat:,.2f})")
    print(f"Editor con mayor ingreso esperado: {max_edit} (${max_val_edit:,.2f})")
    
    print("\nTop 10 Videojuegos con mayor ingreso esperado:")
    limite = min(10, len(lista_juegos_proyeccion))
    for i in range(limite):
        print(f"{i+1}. {lista_juegos_proyeccion[i]['titulo']}: ${lista_juegos_proyeccion[i]['ingreso']:,.2f}")


def ejecutar_requerimiento_5(juegos_dict, inv_dict):
    print("\n--- REQUERIMIENTO 5: ÍNDICE ESTRATÉGICO POR PLATAFORMA ---")
    data_plat = {}
    
    for id_juego, datos in juegos_dict.items():
        plat = datos["plataforma"]
        if plat not in data_plat:
            data_plat[plat] = {"precios": [], "stock_total": 0, "multiplayer_cant": 0, "juegos_cant": 0}
            
        data_plat[plat]["precios"].append(float(datos["precio"]))
        data_plat[plat]["juegos_cant"] += 1
        if datos["multiplayer"]:
            data_plat[plat]["multiplayer_cant"] += 1
            
        registro_inv = buscar_juego_en_inventario(id_juego, inv_dict)
        if registro_inv is not None:
            data_plat[plat]["stock_total"] += int(registro_inv["stock_actual"])
            
    lista_iep = []
    for plat, info in data_plat.items():
        precio_prom = sum(info["precios"]) / len(info["precios"])
        pct_multi = (info["multiplayer_cant"] / info["juegos_cant"]) * 100.0
        
        iep = (precio_prom * 0.35) + (info["stock_total"] * 0.20) + (pct_multi * 0.25) + (info["juegos_cant"] * 0.20)
        lista_iep.append({"plataforma": plat, "iep": iep})
        
    if len(lista_iep) < 2:
        print("Error: No existen suficientes plataformas diferentes para realizar comparaciones.")
        return
        
    lista_iep = ordenar_por_llave_descendente(lista_iep, "iep")
    
    print("Resultados de IEP de Mayor a Menor:")
    for registro in lista_iep:
        print(f"- {registro['plataforma']}: {registro['iep']:.2f} puntos")
        
    primera = lista_iep[0]
    segunda = lista_iep[1]
    
    print(f"\nPlataforma más atractiva: {primera['plataforma']}")
    dif_pct = ((primera["iep"] - segunda["iep"]) / segunda["iep"]) * 100.0
    print(f"Diferencia porcentual con la segunda posición ({segunda['plataforma']}): {dif_pct:.2f}%")


def ejecutar_requerimiento_6(juegos_dict, inv_dict):
    print("\n--- REQUERIMIENTO 6: MOTOR DE RECOMENDACIÓN ---")
    plat_fav = input("Plataforma favorita: ")
    genero_fav = input("Género favorito: ")
    clasi_max = input("Clasificación máxima aceptada (E, T, M): ").upper()
    try:
        presupuesto = float(input("Presupuesto disponible: "))
    except ValueError:
        print("Error: Presupuesto debe ser un número decimal válido.")
        return
        
    jerarquia = {"E": 1, "T": 2, "M": 3}
    if clasi_max not in jerarquia:
        print("Error: Clasificación ingresada no existe.")
        return
        
    recomendaciones = []
    for id_juego, datos in juegos_dict.items():
        registro_inv = buscar_juego_en_inventario(id_juego, inv_dict)
        if registro_inv is not None:
            if jerarquia[datos["clasificacion"]] > jerarquia[clasi_max]:
                continue
                
            stock = int(registro_inv["stock_actual"])
            puntaje = 0
            
            if datos["plataforma"].lower() == plat_fav.lower(): puntaje += 50
            if datos["genero"].lower() == genero_fav.lower(): puntaje += 30
            if datos["multiplayer"]: puntaje += 15
            if float(datos["precio"]) <= presupuesto: puntaje += 10
            puntaje += (5 * stock)
            
            recomendaciones.append({
                "titulo": datos["titulo"],
                "precio": float(datos["precio"]),
                "stock": stock,
                "puntaje": puntaje
            })
            
    recomendaciones = ordenar_recomendaciones_avanzado(recomendaciones)
    
    print("\nVideojuegos Recomendados:")
    for r in recomendaciones:
        print(f"- {r['titulo']} | Puntaje: {r['puntaje']} (Stock: {r['stock']}, Precio: ${r['precio']:.0f})")


def ejecutar_requerimiento_7(juegos_dict, inv_dict):
    print("\n--- REQUERIMIENTO 7: SIMULACIÓN DE EXPANSIÓN ---")
    data_plat = {}
    
    for id_juego, datos in juegos_dict.items():
        plat = datos["plataforma"]
        if plat not in data_plat:
            data_plat[plat] = {"precios": [], "stock_total": 0, "multiplayer_cant": 0, "juegos_cant": 0, "valor_inventario": 0.0}
            
        data_plat[plat]["precios"].append(float(datos["precio"]))
        data_plat[plat]["juegos_cant"] += 1
        if datos["multiplayer"]:
            data_plat[plat]["multiplayer_cant"] += 1
            
        registro_inv = buscar_juego_en_inventario(id_juego, inv_dict)
        if registro_inv is not None:
            stock = int(registro_inv["stock_actual"])
            data_plat[plat]["stock_total"] += stock
            data_plat[plat]["valor_inventario"] += (float(datos["precio"]) * stock)
            
    plataformas_pi = []
    suma_pi_global = 0.0
    
    for plat, info in data_plat.items():
        precio_prom = sum(info["precios"]) / len(info["precios"])
        pct_multi = (info["multiplayer_cant"] / info["juegos_cant"]) * 100.0
        
        pi = info["valor_inventario"] + (precio_prom * info["juegos_cant"]) + (info["stock_total"] * 500.0) + (pct_multi * 1000.0)
        plataformas_pi.append({"plataforma": plat, "pi": pi})
        suma_pi_global += pi
        
    if not plataformas_pi:
        print("No existen datos procesables.")
        return
        
    prom_pi_global = suma_pi_global / len(plataformas_pi)
    
    suma_dif_cuadrado = 0.0
    for p in plataformas_pi:
        suma_dif_cuadrado += (p["pi"] - prom_pi_global) ** 2
        
    varianza = suma_dif_cuadrado / len(plataformas_pi)
    desviacion_estandar = varianza ** 0.5
    
    plataformas_pi = ordenar_por_llave_descendente(plataformas_pi, "pi")
    
    print(f"Plataforma Líder: {plataformas_pi[0]['plataforma']} ({plataformas_pi[0]['pi']:.2f})")
    print(f"Plataforma Menos Atractiva: {plataformas_pi[-1]['plataforma']} ({plataformas_pi[-1]['pi']:.2f})")
    print(f"Promedio Global PI: {prom_pi_global:.2f} | Desviación Estándar: {desviacion_estandar:.2f}")
    
    print("\nPlataformas sobre una desviación estándar del promedio:")
    umbral = prom_pi_global + desviacion_estandar
    ninguna = True
    for p in plataformas_pi:
        if p["pi"] > umbral:
            print(f"- {p['plataforma']} (PI: {p['pi']:.2f})")
            ninguna = False
    if ninguna:
        print("- Ninguna plataforma supera el umbral.")
        
    print("\nRANKING FINAL DE INVERSIÓN:")
    for i, p in enumerate(plataformas_pi):
        print(f"{i+1}. {p['plataforma']} - PI: {p['pi']:.2f}")

def main():
    juegos = {
        1: {"titulo": "Zelda: TotK", "plataforma": "Switch", "precio": 60000.0, "clasificacion": "T", "multiplayer": False, "editor": "Nintendo", "genero": "Aventura"},
        2: {"titulo": "Zelda: TotK", "plataforma": "PS5", "precio": 65000.0, "clasificacion": "T", "multiplayer": False, "editor": "Nintendo", "genero": "Aventura"},
        3: {"titulo": "GTA V", "plataforma": "PS5", "precio": 35000.0, "clasificacion": "M", "multiplayer": True, "editor": "Rockstar", "genero": "Acción"},
        4: {"titulo": "FIFA 26", "plataforma": "PS5", "precio": 250000.0, "clasificacion": "E", "multiplayer": True, "editor": "EA Sports", "genero": "Deportes"},
        5: {"titulo": "Minecraft", "plataforma": "PC", "precio": 25000.0, "clasificacion": "E", "multiplayer": True, "editor": "Mojang", "genero": "Sandbox"},
        6: {"titulo": "GTA V", "plataforma": "PC", "precio": 30000.0, "clasificacion": "M", "multiplayer": True, "editor": "Rockstar", "genero": "Acción"},
        7: {"titulo": "Juego Fantasma", "plataforma": "PC", "precio": 15000.0, "clasificacion": "T", "multiplayer": False, "editor": "Indie", "genero": "Arcade"}
    }

    inventario = {
        1: {"stock_actual": 5},
        2: {"stock_actual": 12},
        3: {"stock_actual": 8},
        4: {"stock_actual": 2},
        5: {"stock_actual": 50},
        6: {"stock_actual": 15},
        8: {"stock_actual": 20}
    }

    while True:
        mostrar_menu()
        opcion = leer_opcion() 
        
        if opcion == -1:
            continue
            
        if opcion == 1:
            ejecutar_requerimiento_1(juegos, inventario)
        elif opcion == 2:
            ejecutar_requerimiento_2(juegos, inventario)
        elif opcion == 3:
            ejecutar_requerimiento_3(juegos, inventario)
        elif opcion == 4:
            ejecutar_requerimiento_4(juegos, inventario)
        elif opcion == 5:
            ejecutar_requerimiento_5(juegos, inventario)
        elif opcion == 6:
            ejecutar_requerimiento_6(juegos, inventario)
        elif opcion == 7:
            ejecutar_requerimiento_7(juegos, inventario)
        elif opcion == 8:
            print("\nCerrando Módulo SICV de GameHub Analytics. ¡Mucho éxito en la evaluación!")
            break 

main()