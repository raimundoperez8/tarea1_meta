from numpy import *
import random
import linecache as lc
import time


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

    #se preparan las variables del problema, en matrices y listas
    drones, delays, tot = lectura(test)

    for i in range(len(drones)):
        temp = drones[i]
        temp = temp.split(" ")
        drones[i] = temp
    for i in range(len(delays)):
        temp = delays[i]
        temp = temp.split(" ")
        delays[i] = temp

    #se ordenan los drones segun su tiempo maximo de envio, es decir, los que "caducan" antes, quedan primero
    drones.sort(key = lambda x: x[3])

    #para cada uno de los drones
    for i in range(tot):

        #el dron no es el ultimo
        if (i + 1 < tot):
            
            #se verifica si el tiempo optimo del dron actual es mayor al tiempo actual del ejercicio
            if int(drones[i][2]) >= timeline:
                
                #tiempo optimo posible, por lo tanto, el dron se envia en su tiempo optimo y se ajusta el timeline
                if int(drones[i+1][3]) >= int(drones[i][2]) + int(delays[int(drones[i][0])][int(drones[i+1][0])]):    
                    timeline = int(drones[i][2])
                    res = [drones[i][0], timeline]
                    resultado.append(res)

                    #diferencia entre el optimo y el tiempo del dron (0), se suma a los costos
                    suma += abs(int(drones[i][2]) - timeline)

                    #a la linea de tiempo, se le suma el tiempo de espera obligatorio minimo para el siguiente dron
                    timeline = timeline + int(delays[int(drones[i][0])][int(drones[i+1][0])])
                    agregados +=1

                #optimo "mata" al siguiente dron, impidiendo su envio, por lo que el dron se envia en el tiempo actual 
                elif (timeline + int(delays[int(drones[i][0])][int(drones[i+1][0])]) >= int(drones[i+1][3])):
                    res = [drones[i][0], timeline]
                    resultado.append(res)

                    #diferencia entre el optimo y el tiempo de envio del dron se suma a los costos
                    suma += abs(int(drones[i][2]) - timeline)
                    timeline = timeline + int(delays[int(drones[i][0])][int(drones[i+1][0])])
                    agregados +=1

            #el optimo ya paso, por lo que el dron se envia simplemente
            else:
                res = [drones[i][0], timeline]
                resultado.append(res)

                #diferencia entre el optimo y el tiempo de envio del dron se suma a los costos
                suma += abs(int(drones[i][2]) - timeline)
                timeline = timeline + int(delays[int(drones[i][0])][int(drones[i+1][0])])
                agregados +=1
        
        #el ultimo dron
        else:
            #corresponde al ultimo dron, por lo que simplemente se envia
            res = [drones[i][0], timeline]
            resultado.append(res)

            #diferencia entre el optimo y el tiempo de envio del dron se suma a los costos
            suma += abs(int(drones[i][2]) - timeline)
            agregados +=1

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
    drones, delays, tot = lectura(test)

    for i in range(len(drones)):
        temp = drones[i]
        temp = temp.split(" ")
        drones[i] = temp
    for i in range(len(delays)):
        temp = delays[i]
        temp = temp.split(" ")
        delays[i] = temp

    #se ordenan los drones segun su tiempo maximo de envio, es decir, los que "caducan" antes, quedan primero
    drones.sort(key = lambda x: x[3])

    #Se crea un nuevo array modificado, buscando agrupar los tiempos de termino (redondeando hacia abajo)
    #Es decir, se considera que los drones que terminan dentro de cierto intervalo, son "iguales"
    #Al ser "iguales", se puede seleccionar cualquiera de ellos en el intervalo en cuestion
    for i in range(len(drones)):
        drontemp = drones[i].copy()
        temp = int(drontemp[3])
        temp = int(temp/100)
        temp = temp*100
        drontemp[3] = temp
        dronesmod.append(drontemp)

    #Cuenta los grupos generados segun el metodo anterior, comentar al tener el programa listo (Mantener en el codigo)
    #Es utilizado en las fases de prueba, buscando un valor universal para generar la agrupacion anterior (es decir, que sea util)
    contar_term = {}

    for i in range(tot):
        if (dronesmod[i][3] not in contar_term.keys()):
            contar_term[dronesmod[i][3]] = 1
        else:
            contar_term[dronesmod[i][3]] += 1

    #Se crea una matriz, de distintos arrays, agrupando los drones segun su nuevo tiempo de "termino"
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


    #Se aplica una logica similar a la anterior:    
    indice = 0
    for i in range(tot):
        #se elige un dron aleatoriamente dentro del grupo correspondiente
        numero_dron = random.randint(0, len(agrupacion[indice])-1)

        #Se debe Actualizar el timeline en base al dron agregado anteriormente y el elegido actual
        if (len(resultado) > 0):

            #En el array delay del dron previamente agregado a la solucion (si existe),
            #se busca y se agrega la diferencia minima requerida para poder enviar el dron elegido
            del_anterior = delays[int(resultado[-1][0])]
            espera_actual = del_anterior[int(agrupacion[indice][numero_dron][0])]
            timeline = timeline + int(espera_actual)

        #el dron no es el ultimo
        if (i + 1 < tot):

            #se verifica si el tiempo optimo del dron actual es mayor al tiempo actual del ejercicio
            if int(agrupacion[indice][numero_dron][2]) >= timeline:
                
                #Comparte intervalo
                if (len(agrupacion[indice]) > 1):
                    #Calcular si el optimo es posible
                    posible = 1

                    #Se revisa si utilizar el tiempo optimo "mata" a algun dron restante en el grupo, impidiendo su envio
                    #En caso de hacerlo, posible = 0, pues no es conveniente hacerlo
                    for j in range(len(agrupacion[indice])):
                        if (j == numero_dron):
                            continue
                        else:
                            lista_del = delays[int(agrupacion[indice][numero_dron][0])]
                            diferencia = int(agrupacion[indice][numero_dron][2])
                            diferencia += int(lista_del[int(agrupacion[indice][j][0])])
                            
                            if (int(drones[int(agrupacion[indice][j][0])][3]) - diferencia < 0):
                                posible = 0

                    #tiempo optimo posible, por lo tanto, el dron se envia en su tiempo optimo y se ajusta el timeline
                    if (posible):
                        timeline = int(agrupacion[indice][numero_dron][2])
                        res = [agrupacion[indice][numero_dron][0], timeline]
                        resultado.append(res)

                        #diferencia entre el optimo y el tiempo del dron (0), se suma a los costos
                        suma += abs(int(agrupacion[indice][numero_dron][2]) - timeline)
                        agregados +=1

                        #Se elimina el elemento agregado del grupo correspondiente
                        agrupacion[indice].pop(numero_dron)

                        #Si el intervalo se vacia, se pasa al siguiente
                        if (len(agrupacion[indice]) == 0):
                            indice += 1

                    else:
                        res = [agrupacion[indice][numero_dron][0], timeline]
                        resultado.append(res)

                        #diferencia entre el optimo y el tiempo del dron (0), se suma a los costos
                        suma += abs(int(agrupacion[indice][numero_dron][2]) - timeline)
                        agregados +=1
                        
                        #Se elimina el elemento agregado del grupo correspondiente
                        agrupacion[indice].pop(numero_dron)

                        #Si el intervalo se vacia, se pasa al siguiente
                        if (len(agrupacion[indice]) == 0):
                            indice += 1

                #Es el Unico/Ultimo dron en el intervalo actual
                #Se envia el dron en el tiempo optimo correspondiente
                else:
                    timeline = int(agrupacion[indice][numero_dron][2])
                    res = [agrupacion[indice][numero_dron][0], timeline]
                    resultado.append(res)

                    #diferencia entre el optimo y el tiempo de envio del dron se suma a los costos
                    suma += abs(int(agrupacion[indice][numero_dron][2]) - timeline)
                    agregados +=1

                    #Se elimina el elemento agregado del grupo correspondiente
                    agrupacion[indice].pop(numero_dron)

                    #Si el intervalo se vacia, se pasa al siguiente
                    if (len(agrupacion[indice]) == 0):
                        indice += 1

            #el optimo ya paso, por lo que el dron se envia simplemente
            else:                
                res = [agrupacion[indice][numero_dron][0], timeline]
                resultado.append(res)

                #diferencia entre el optimo y el tiempo de envio del dron se suma a los costos
                suma += abs(int(agrupacion[indice][numero_dron][2]) - timeline)
                agregados +=1

                #Se elimina el elemento agregado del grupo correspondiente
                agrupacion[indice].pop(numero_dron)

                #Si el intervalo se vacia, se pasa al siguiente
                if (len(agrupacion[indice]) == 0):
                    indice += 1
        
        #el ultimo dron
        else:

            #corresponde al ultimo dron, por lo que simplemente se envia
            res = [agrupacion[indice][0][0], timeline]
            resultado.append(res)

            #diferencia entre el optimo y el tiempo de envio del dron se suma a los costos
            suma += abs(int(agrupacion[indice][0][2]) - timeline)
            agregados +=1

    resultado.append(suma)
    print("Solucion Greedy Estoc:")
    print(resultado)
    print(agregados)
    return resultado


#Funcion para obtener el costo de una solucion
def genera_costo_sol(vecino, delays, drones):
    suma = 0

    #se suma la diferencia entre el tiempo de envio y el optimo, para cada dron
    for dron in vecino:        
        id = dron[0]
        tiempo = dron[1]
        suma += abs(int(tiempo) - int(drones[int(id)][2]))
    
    #Validate_sol(): if invalida suma += 200 en cada caso
    flag = 0
    for i in range(len(vecino)-1):
        #se verifica que el dron haya sido enviado dentro del plazo
        if int(drones[int(vecino[i][0])][1]) <= int(vecino[i][1]) and int(drones[int(vecino[i][0])][3]) >= int(vecino[i][1]):
            flag = 0
        else:
            flag = 200
        #se verifica que el tiempo minimo entre drones se cumpla
        if int(vecino[i][1]) + int(delays[int(vecino[i][0])][int(vecino[i+1][0])]) <= int(vecino[i+1][1]):
            flag += 0
        else:
            flag += 200

    return suma + flag


#Funcion para obtener los vecinos de una solucion determinada
#Se generan nuevas soluciones (factible o no) en base a una solucion dada
def genera_vecinos(solucion):
    vecinos = []
    for i in range(len(solucion)):
        for j in range(i + 1, len(solucion)):
            vecino = solucion.copy()

            #se genera una perturbacion en base a la semilla entregada a la funcion
            delta1 = random.randint(0,8) - 4
            delta2 = random.randint(0,8) - 4

            #se intercambia el orden de envio de dos drones, y los tiempos se perturban en base al delta generado
            vecino[i] = solucion[j].copy()
            vecino[i][1] = solucion[i][1] + delta1
            vecino[j] = solucion[i].copy()
            vecino[j][1] = solucion[j][1] + delta2
            vecinos.append(vecino)
  
    return vecinos


#En base a las soluciones generadas, se obtiene la mejor de estas, calculando su costo
def obt_mejor_vecino(vecinos, delays, drones):
    mejor_costo = genera_costo_sol(vecinos[0], delays, drones) #costo del primer vecino para iniciarlo
    mejor_vecino = vecinos[0]

    #se comparan todos los costos
    for vecino in vecinos:
        costo_actual = genera_costo_sol(vecino, delays, drones)
        
        if (costo_actual < mejor_costo):
            mejor_costo = costo_actual
            mejor_vecino = vecino

    #se devuelve el mejor (menor) costo
    return mejor_vecino, mejor_costo


def hill_climbing_AM(test, sol_inicial, seed = 0):

    #se fija la semilla a utilizar, entregada como parametro
    random.seed(seed)

    #se preparan las variables del problema, en matrices y listas
    drones, delays, tot = lectura(test)

    for i in range(len(drones)):
        temp = drones[i]
        temp = temp.split(" ")
        drones[i] = temp
    for i in range(len(delays)):
        temp = delays[i]
        temp = temp.split(" ")
        delays[i] = temp

    #se separa el costo y solucion inicial entregados como parametros
    costo_inicial = sol_inicial[len(sol_inicial)-1]
    sol_inicial.pop(len(sol_inicial)-1)

    sol_actual = sol_inicial
    costo_actual = costo_inicial

    #a partir de la solucion entregada, se generan los vecinos de esta
    vecinos_actuales = genera_vecinos(sol_actual)

    #se guarda el mejor vecino de la lista de vecinos
    mejor_vecino, mejor_costo = obt_mejor_vecino(vecinos_actuales, delays, drones)

    #si el vecino encontrado es mejor que la solucion actual:
    #si esto no ocurre, estamos en el optimo local
    while mejor_costo < costo_actual:

        #reemplazamos la solucion/costo actuales por los nuevos solucion/costo (se mejora la solucion)
        sol_actual = mejor_vecino
        costo_actual = mejor_costo

        #a partir de la solucion entregada, se generan los vecinos de esta
        vecinos_actuales = genera_vecinos(sol_actual)
        mejor_vecino, mejor_costo = obt_mejor_vecino(vecinos_actuales, delays, drones)

        #habiendo mejorado, y pudiendo mejorar de nuevo, el agoritmo termina
        #puesto que ya se hizo una mejora (lo pedido)
        if mejor_costo < costo_actual:
            break

    sol_actual.append(costo_actual)    
    print("solucion Hill AM:")
    print(sol_actual)

    return sol_actual


def hill_climbing_MM(test, sol_inicial, seed = 0):

    #se fija la semilla a utilizar, entregada como parametro
    random.seed(seed)

    #se preparan las variables del problema, en matrices y listas
    drones, delays, tot = lectura(test)

    for i in range(len(drones)):
        temp = drones[i]
        temp = temp.split(" ")
        drones[i] = temp
    for i in range(len(delays)):
        temp = delays[i]
        temp = temp.split(" ")
        delays[i] = temp

    #se separa el costo y solucion inicial entregados como parametros
    costo_inicial = sol_inicial[len(sol_inicial)-1]
    sol_inicial.pop(len(sol_inicial)-1)

    sol_actual = sol_inicial
    costo_actual = costo_inicial

    #a partir de la solucion entregada, se generan los vecinos de esta
    vecinos_actuales = genera_vecinos(sol_actual)

    #se guarda el mejor vecino de la lista de vecinos
    mejor_vecino, mejor_costo = obt_mejor_vecino(vecinos_actuales, delays, drones)

    #se inicia el timer, con el fin de poder cumplir con el TO de 180s
    t_inicio = time.time()

    #si el vecino encontrado es mejor que la solucion actual:
    #si esto no ocurre, estamos en el optimo local.
    #En otras palabras, el algoritmo mejorara la solucion hasta el TO o hasta estar en el optimo local
    while mejor_costo < costo_actual:

        #reemplazamos la solucion/costo actuales por los nuevos solucion/costo (se mejora la solucion)
        sol_actual = mejor_vecino
        costo_actual = mejor_costo

        #a partir de la solucion entregada, se generan los vecinos de esta
        #y se obtiene el mejor vecino-costo entre estos
        vecinos_actuales = genera_vecinos(sol_actual)
        mejor_vecino, mejor_costo = obt_mejor_vecino(vecinos_actuales, delays, drones)

        #se revisa la condicion de TO
        t_actual = time.time()
        if (t_actual-t_inicio > 180):
            break

    sol_actual.append(costo_actual) 
    print("solucion Hill MM:")
    print(sol_actual)

    return sol_actual


def tabu_search(test, sol_inicial, size = 3, seed = 0):

    #se fija la semilla a utilizar. Al no ser entregada, tendra valor 0
    random.seed(seed)

    #se preparan las variables del problema, en matrices y listas
    drones, delays, tot = lectura(test)

    for i in range(len(drones)):
        temp = drones[i]
        temp = temp.split(" ")
        drones[i] = temp
    for i in range(len(delays)):
        temp = delays[i]
        temp = temp.split(" ")
        delays[i] = temp

    #se separa el costo y solucion inicial entregados como parametros
    costo_inicial = sol_inicial[len(sol_inicial)-1]
    sol_inicial.pop(len(sol_inicial)-1)

    #tabu logic

    solution = sol_inicial    
    best_cost = costo_inicial
    tabu_list = list()

    best_solution_ever = solution

    #se inicia el timer, con el fin de poder cumplir con el TO de 180s
    t_actual = 0
    t_inicio = time.time()

    #a partir de la solucion entregada, se generan los vecinos de esta
    vecinos_actuales = genera_vecinos(solution)

    #se guarda el mejor vecino de la lista de vecinos
    mejor_vecino, mejor_costo = obt_mejor_vecino(vecinos_actuales, delays, drones)

    #0 = No se ha aceptado un movimiento (el movimiento esta en la lista tabu)
    #1 = El movimiento es valido (no esta en la lista tabu)
    #parte como 1, pues la lista tabu inicialmente esta vacia
    movimiento = 1

    #se revisa la condicion de TO
    while (t_actual-t_inicio < 180):

        if movimiento == 1:
            #al poder generar el desplazamiento, se generan los vecinos de la nueva solucion
            vecinos_actuales = genera_vecinos(solution)
            #se busca el mejor de los nuevos vecinos
            mejor_vecino, mejor_costo = obt_mejor_vecino(vecinos_actuales, delays, drones)

            best_solution = mejor_vecino
        else:
            #al no poder realizarse el movimiento, se busca un nuevo candidato en la lista de vecinos actuales
            mejor_vecino, mejor_costo = obt_mejor_vecino(vecinos_actuales, delays, drones)
            best_solution = mejor_vecino
        
        #teniendo un movimiento candidato, se busca a que movimiento corresponde dicho vecino candidato
        #(permutacion en el orden de envio de los drones)
        found = False
        while found is False:
            i = 0
            while i < len(best_solution):
 
                if best_solution[i][0] != solution[i][0]:
                    first_exchange_node = best_solution[i][0]
                    second_exchange_node = solution[i][0]

                    #se almacena el dron intercambiado y la posicion asociada
                    indice_c = i
                    valor_c = best_solution[i][0]
                    break
                i = i + 1

            #se revisa la condicion de TO
            t_actual = time.time()
            if (t_actual-t_inicio > 180):
                break

            #se verifica si el movimiento (o su reciproco) se encuentra en la lista tabu
            #al no estar, se agrega y se acepta el movimiento (movimiento = 1)
            if [first_exchange_node, second_exchange_node] not in tabu_list and [
                second_exchange_node,
                first_exchange_node,
            ] not in tabu_list:
                tabu_list.append([first_exchange_node, second_exchange_node])
                found = True
                movimiento = 1

                #se realiza el movimiento, actualizando la solucion actual/mejor solucion
                solution = best_solution
                cost = mejor_costo
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
                
            #movimiento en lista tabu
            else:
                #ignorar movimiento, ver siguiente opcion
                movimiento = 0

                #se busca el movimiento candidato en la lista de vecinos
                for mov in vecinos_actuales:
                    
                    #se elimina el candidato de la lista, pues es un candidato "invalido"
                    #esto gracias al almacenamiento previo de dron-posicion guardados
                    if (mov[indice_c][0] == valor_c):

                        indice = vecinos_actuales.index(mov)
                        del vecinos_actuales[indice]
                        break

                #la mejor solucion corresponde a la mejor solucion previa (es decir, se ignora la solucion encontrada)
                best_solution = solution

        #si la lista tabu supera su tamano asignado, se elimina el elemento mas viejo de esta
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

def main():
    #casos de prueba
    test3 = "t2_Deimos.txt"
    test2 = "t2_Europa.txt"
    test1 = "t2_Titan.txt"

    flag = True

    while flag:
        tecnica = -1
        caso = -1
        semilla = -1
        sol_inicial = -1
        exit = -1

        while tecnica not in range(1,6):
            tecnica = int(input("Elige la tecnica a utilizar:\n 1.Greedy determinista\n 2.Greedy estocastico\n 3.Hill-climbing AM\n 4.Hill-climbing MM\n 5.Tabu Search\n"))
        while caso not in range(1,4):
            caso = int(input("Elige caso de prueba a utilizar (15, 30 o 100 UAVs -> 1-2-3): "))
        while semilla not in range(0,5):
            semilla = int(input("Elige la semilla a utilizar (entre 0 y 4): "))
        
        if caso == 1:
            test = test1
        if caso == 2:
            test = test2
        if caso == 3:
            test = test3

        if tecnica in range(3,6):
            while sol_inicial not in range(1,3):
                sol_inicial = int(input("¿Que solucion inicial deseas utilizar?:\n 1.Determinista\n 2.Estocastica\n"))
                if sol_inicial == 1:
                    solucion_ini = greedy_det(test)
                elif sol_inicial == 2:
                    solucion_ini = greedy_estoc(test, semilla)

        if tecnica == 1:
            greedy_det(test)
        if tecnica == 2:
            greedy_estoc(test, semilla)
        if tecnica == 3:
            hill_climbing_AM(test, solucion_ini, semilla)
        if tecnica == 4:
            hill_climbing_MM(test, solucion_ini, semilla)
        if tecnica == 5:
            tabu_search(test, solucion_ini, semilla)
        
        while exit not in range(1,3):
            exit = int(input("¿Deseas finalizar las pruebas?\n 1.si\n 2.no\n"))
        
        if (exit == 1):
            flag = False

if __name__ == "__main__":
    main()
