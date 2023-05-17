from numpy import *
import random
import linecache as lc
import time

test3 = "t2_Deimos.txt"
test2 = "t2_Europa.txt"
test1 = "t2_Titan.txt"


def lectura(test):
    drones = []
    delays = []

    f = open(test)
    cont  = 0
    tot = lc.getline(test, 1)
    tot = int(tot)
    linea = 2

    while (cont < tot):
        drones.append(str(cont) + " " + lc.getline(test, linea).strip())
        delays.append(lc.getline(test, linea + 1).strip())
        cont += 1
        linea += 2

    return drones, delays, tot


def greedy_det(test):
    agregados = 0
    timeline = 0
    resultado = []
    suma = 0

    drones, delays, tot = lectura(test)

    for i in range(len(drones)):
        temp = drones[i]
        temp = temp.split(" ")
        drones[i] = temp

    for i in range(len(delays)):
        temp = delays[i]
        temp = temp.split(" ")
        delays[i] = temp

    drones.sort(key = lambda x: x[3])
    #print(drones)
    for i in range(tot):
        #print(i)
        if (i + 1 < tot):
            #print(i)
            if int(drones[i][2]) >= timeline:
                

                #tiempo optimo posible
                if int(drones[i+1][3]) >= int(drones[i][2]) + int(delays[int(drones[i][0])][int(drones[i+1][0])]):    
                    timeline = int(drones[i][2])
                    res = [drones[i][0], timeline]
                    resultado.append(res)

                    #diferencia entre el optimo y el tiempo del dron
                    suma += abs(int(drones[i][2]) - timeline)
                    timeline = timeline + int(delays[int(drones[i][0])][int(drones[i+1][0])])
                    agregados +=1

                #optimo "mata" al siguiente dron
                elif (timeline + int(delays[int(drones[i][0])][int(drones[i+1][0])]) >= int(drones[i+1][3])):
                    res = [drones[i][0], timeline]
                    resultado.append(res)

                    #diferencia entre el optimo y el tiempo del dron
                    suma += abs(int(drones[i][2]) - timeline)
                    timeline = timeline + int(delays[int(drones[i][0])][int(drones[i+1][0])])
                    agregados +=1


            #el optimo ya paso
            else:
                #print(i)
                #print(res)
                res = [drones[i][0], timeline]
                resultado.append(res)

                #diferencia entre el optimo y el tiempo del dron
                suma += abs(int(drones[i][2]) - timeline)
                timeline = timeline + int(delays[int(drones[i][0])][int(drones[i+1][0])])
                agregados +=1

        else:
            #el ultimo dron
            res = [drones[i][0], timeline]
            resultado.append(res)

            #diferencia entre el optimo y el tiempo del dron
            suma += abs(int(drones[i][2]) - timeline)
            agregados +=1

    #[[ndron, tiempo], costo]
    resultado.append(suma)
    print("Solucion Greedy det:")
    print(resultado)
    print(agregados)
    return resultado


def greedy_estoc(test, seed):

    ##################
    #Variables y setup
    ##################

    random.seed(seed)
    timeline = 0 
    agregados = 0  
    suma = 0
    resultado = []
    dronesmod = []

    ##################
    #Setup

    drones, delays, tot = lectura(test)

    for i in range(len(drones)):
        temp = drones[i]
        temp = temp.split(" ")
        drones[i] = temp

    for i in range(len(delays)):
        temp = delays[i]
        temp = temp.split(" ")
        delays[i] = temp

    drones.sort(key = lambda x: x[3])

    ##################
    ##################
    #aqui el algoritmo

    #Se crea un nuevo array modificado, buscando agrupar los tiempos de termino
    for i in range(len(drones)):
        drontemp = drones[i].copy()
        temp = int(drontemp[3])
        temp = int(temp/100)
        temp = temp*100
        drontemp[3] = temp
        dronesmod.append(drontemp)

    ######################################
    ######################################
    #Cuenta los grupos generados segun el metodo anterior, comentar al tener el programa listo (Mantener en el codigo)
    contar_term = {}

    for i in range(tot):
        if (dronesmod[i][3] not in contar_term.keys()):
            contar_term[dronesmod[i][3]] = 1
        else:
            contar_term[dronesmod[i][3]] += 1

    ######################################
    ######################################

    ######################################
    #> Agrupar los datos segun su termino
    termino = -1
    indice = -1
    agrupacion = []
    
    for i in range(tot):
        if (termino != dronesmod[i][3]):
            termino = dronesmod[i][3]
            agrupacion.append([])
            indice += 1
            agrupacion[indice].append(dronesmod[i])
        else:
            agrupacion[indice].append(dronesmod[i])

    ######################################  
    #> Aplicar logica similar a la anterior:
    
    indice = 0

    for i in range(tot):
        numero_dron = random.randint(0, len(agrupacion[indice])-1)

        #Actualizar timeline en base al dron agregado anterior mente y el elegido actual
        if (len(resultado) > 0):
            #En el array delay del dron anterior, agregar la diferencia requeria por el dron actual
            del_anterior = delays[int(resultado[-1][0])]
            espera_actual = del_anterior[int(agrupacion[indice][numero_dron][0])]
            timeline = timeline + int(espera_actual)

        if (i + 1 < tot):
            #Optimo > Timeline
            if int(agrupacion[indice][numero_dron][2]) >= timeline:
                #Comparte intervalo
                if (len(agrupacion[indice]) > 1):
                    #Calcular si el optimo es posible
                    posible = 1

                    for j in range(len(agrupacion[indice])):
                        if (j == numero_dron):
                            continue
                        else:
                            lista_del = delays[int(agrupacion[indice][numero_dron][0])]
                            diferencia = int(agrupacion[indice][numero_dron][2])
                            diferencia += int(lista_del[int(agrupacion[indice][j][0])])
                            
                            if (int(drones[int(agrupacion[indice][j][0])][3]) - diferencia < 0):
                                posible = 0

                    if (posible):
                        timeline = int(agrupacion[indice][numero_dron][2])
                        res = [agrupacion[indice][numero_dron][0], timeline]
                        resultado.append(res)
                        suma += abs(int(agrupacion[indice][numero_dron][2]) - timeline)
                        agregados +=1
                        agrupacion[indice].pop(numero_dron)

                        if (len(agrupacion[indice]) == 0):
                            indice += 1

                    else:
                        res = [agrupacion[indice][numero_dron][0], timeline]
                        resultado.append(res)
                        suma += abs(int(agrupacion[indice][numero_dron][2]) - timeline)
                        agregados +=1
                        #Se elimina el elemento agregado
                        agrupacion[indice].pop(numero_dron)

                        if (len(agrupacion[indice]) == 0):
                            indice += 1

                #Unico/Ultimo en intervalo
                #Apuesto por el optimo
                else:
                    timeline = int(agrupacion[indice][numero_dron][2])
                    res = [agrupacion[indice][numero_dron][0], timeline]
                    resultado.append(res)
                    suma += abs(int(agrupacion[indice][numero_dron][2]) - timeline)
                    agregados +=1
                    agrupacion[indice].pop(numero_dron)

                    if (len(agrupacion[indice]) == 0):
                        indice += 1

            #el optimo ya paso
            else:
                res = [agrupacion[indice][numero_dron][0], timeline]
                resultado.append(res)
                suma += abs(int(agrupacion[indice][numero_dron][2]) - timeline)
                agregados +=1
                #Se elimina el elemento agregado
                agrupacion[indice].pop(numero_dron)

                if (len(agrupacion[indice]) == 0):
                    indice += 1

        else:
            #el ultimo dron
            res = [agrupacion[indice][0][0], timeline]
            resultado.append(res)
            suma += abs(int(agrupacion[indice][0][2]) - timeline)
            agregados +=1

    #[[ndron, tiempo], costo]
    resultado.append(suma)
    print("Solucion Greedy Estoc:")
    print(resultado)
    print(agregados)
    return resultado

    #> Aplicar logica similar a la anterior:
    #Selecciono uno del grupo al azar, veo si lo puedo mandar en el optimo sin matar al resto del grupo, lo añado en tiempo x (aqui hay que pensar un par de cosas)
    #Una vez termino el grupo, siguiente grupo

    #####


#Funcion para obtener el costo de una solucion
def genera_costo_sol(vecino, delays, drones):
    suma = 0

    for dron in vecino:
        
        id = dron[0]
        tiempo = dron[1]
        suma += abs(int(tiempo) - int(drones[int(id)][2]))

    
    #Validate_sol(): if incalida suma += 100?
    flag = 0
    for i in range(len(vecino)-1):
        if int(drones[int(vecino[i][0])][1]) <= int(vecino[i][1]) and int(drones[int(vecino[i][0])][3]) >= int(vecino[i][1]):
            flag = 0
        else:
            flag = 200
        if int(vecino[i][1]) + int(delays[int(vecino[i][0])][int(vecino[i+1][0])]) <= int(vecino[i+1][1]):
            flag += 0
        else:
            flag += 200

    return suma + flag


#Funcion para obtener los vecinos de una solucion determinada
def genera_vecinos(solucion):
    vecinos = []
    for i in range(len(solucion)):
        for j in range(i + 1, len(solucion)):
            vecino = solucion.copy()

            delta1 = random.randint(0,8) - 4
            delta2 = random.randint(0,8) - 4

            vecino[i] = solucion[j].copy()
            vecino[i][1] = solucion[i][1] + delta1
            vecino[j] = solucion[i].copy()
            vecino[j][1] = solucion[j][1] + delta2
            vecinos.append(vecino)

    #print("vecinos")
    #print(vecinos[0])
    
    return vecinos


def obt_mejor_vecino(vecinos, delays, drones):
    mejor_costo = genera_costo_sol(vecinos[0], delays, drones) #costo del primer vecino para iniciarlo
    mejor_vecino = vecinos[0]

    for vecino in vecinos:
        costo_actual = genera_costo_sol(vecino, delays, drones)
        
        if (costo_actual < mejor_costo):
            mejor_costo = costo_actual
            mejor_vecino = vecino

    return mejor_vecino, mejor_costo


def hill_climbing_AM(test, sol_inicial, seed):
    random.seed(seed)

    drones, delays, tot = lectura(test)

    for i in range(len(drones)):
        temp = drones[i]
        temp = temp.split(" ")
        drones[i] = temp

    for i in range(len(delays)):
        temp = delays[i]
        temp = temp.split(" ")
        delays[i] = temp


    costo_inicial = sol_inicial[len(sol_inicial)-1]
    sol_inicial.pop(len(sol_inicial)-1)

    sol_actual = sol_inicial
    costo_actual = costo_inicial
    vecinos_actuales = genera_vecinos(sol_actual)
    mejor_vecino, mejor_costo = obt_mejor_vecino(vecinos_actuales, delays, drones)

    #revisar condiciones para seguir iterando
    while mejor_costo < costo_actual:
        sol_actual = mejor_vecino
        costo_actual = mejor_costo
        vecinos_actuales = genera_vecinos(sol_actual)
        mejor_vecino, mejor_costo = obt_mejor_vecino(vecinos_actuales, delays, drones)
        if mejor_costo < costo_actual:
            break

    sol_actual.append(costo_actual) 
    
    print("solucion Hill AM:")
    print(sol_actual)

    return sol_actual


def hill_climbing_MM(test, sol_inicial, seed):
    random.seed(seed)

    drones, delays, tot = lectura(test)

    for i in range(len(drones)):
        temp = drones[i]
        temp = temp.split(" ")
        drones[i] = temp

    for i in range(len(delays)):
        temp = delays[i]
        temp = temp.split(" ")
        delays[i] = temp

    costo_inicial = sol_inicial[len(sol_inicial)-1]
    sol_inicial.pop(len(sol_inicial)-1)

    sol_actual = sol_inicial
    costo_actual = costo_inicial
    vecinos_actuales = genera_vecinos(sol_actual)
    #print(vecinos_actuales)
    mejor_vecino, mejor_costo = obt_mejor_vecino(vecinos_actuales, delays, drones)

    t_inicio = time.time()
    #revisar condiciones para seguir iterando
    while mejor_costo < costo_actual:
        sol_actual = mejor_vecino
        costo_actual = mejor_costo
        vecinos_actuales = genera_vecinos(sol_actual)
        mejor_vecino, mejor_costo = obt_mejor_vecino(vecinos_actuales, delays, drones)
        t_actual = time.time()
        if (t_actual-t_inicio > 180):
            break

    sol_actual.append(costo_actual) 

    print("solucion Hill MM:")
    print(sol_actual)

    return sol_actual



def tabu_search(test, sol_inicial, seed, size=3):
    random.seed(seed)

    drones, delays, tot = lectura(test)

    for i in range(len(drones)):
        temp = drones[i]
        temp = temp.split(" ")
        drones[i] = temp

    for i in range(len(delays)):
        temp = delays[i]
        temp = temp.split(" ")
        delays[i] = temp

    costo_inicial = sol_inicial[len(sol_inicial)-1]
    sol_inicial.pop(len(sol_inicial)-1)


    #tabu logic


    solution = sol_inicial    
    best_cost = costo_inicial
    tabu_list = list()

    best_solution_ever = solution

    t_actual = 0
    t_inicio = time.time()
 
    while (t_actual-t_inicio < 180):

        vecinos_actuales = genera_vecinos(solution)
        mejor_vecino, mejor_costo = obt_mejor_vecino(vecinos_actuales, delays, drones)

        index_of_best_solution = 0

        best_solution = mejor_vecino
        #best_cost_index = len(best_solution) - 1
 
        found = False
        while found is False:
            i = 0
            while i < len(best_solution):
 
                if best_solution[i] != solution[i]:
                    first_exchange_node = best_solution[i]
                    second_exchange_node = solution[i]
                    break
                i = i + 1
                
            t_actual = time.time()
            if (t_actual-t_inicio > 180):
                break
 
            if [first_exchange_node, second_exchange_node] not in tabu_list and [
                second_exchange_node,
                first_exchange_node,
            ] not in tabu_list:
                tabu_list.append([first_exchange_node, second_exchange_node])
                found = True
                solution = best_solution
                cost = mejor_costo
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
            else:
                index_of_best_solution = index_of_best_solution + 1
                best_solution = mejor_vecino
 
        if len(tabu_list) >= size:
            tabu_list.pop(0)
 
        t_actual = time.time()


    best_solution_ever.append(best_cost)

    print("solucion Tabu Search:")
    print(best_solution_ever)
    return best_solution_ever
 






####
#Main
####



#greedy_det(test3)

seed = 1


size = 3

"""
for i in range(5):  
    greedy_estoc(test1, i)

for seed in range(5):

    hill_climbing_AM(test1, greedy_estoc(test1, seed), seed)
"""

hill_climbing_MM(test3, greedy_estoc(test3, seed), seed)


tabu_search(test3, greedy_estoc(test3, seed), seed)