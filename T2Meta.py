from numpy import *
import random
import linecache as lc


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

    print(drones)

    for i in range(tot):

        if (i + 1 < tot):

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
                elif (timeline + int(delays[int(drones[i][0])][int(drones[i+1][0])]) <= int(drones[i+1][3])):

                    res = [drones[i][0], timeline]
                    resultado.append(res)


                    #diferencia entre el optimo y el tiempo del dron
                    suma += abs(int(drones[i][2]) - timeline)
                    timeline = timeline + int(delays[int(drones[i][0])][int(drones[i+1][0])])
                    agregados +=1


            #el optimo ya paso
            else:
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

    #print(drones)
    #print(dronesmod)



    ######################################
    ######################################
    #Cuenta los grupos generados segun el metodo anterior, comentar al tener el programa listo (Mantener en el codigo)
    contar_term = {}
    for i in range(tot):
        if (dronesmod[i][3] not in contar_term.keys()):
            contar_term[dronesmod[i][3]] = 1
        else:
            contar_term[dronesmod[i][3]] += 1
    #print(contar_term)
    #print(len(contar_term.keys()))
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
    
    #print(agrupacion)
    #print(len(agrupacion))


    ######################################  
    #> Aplicar logica similar a la anterior:
    
    indice = 0

    for i in range(tot):
        if (i + 1 < tot):


            numero_dron = random.randint(0, len(agrupacion[indice])-1)
            
            #print(agrupacion[indice])
            #print("numero ", numero_dron)
            #print(len(agrupacion[indice]))
            #print(numero_dron)
            #print(timeline)
            #Actualizar timeline en base al dron agregado anterior mente y el elegido actual
            if (len(resultado) > 0):
                #En el array delay del dron anterior, agregar la diferencia requeria por el dron actual
                del_anterior = delays[int(resultado[-1][0])]
                #print(del_anterior)
                espera_actual = del_anterior[int(agrupacion[indice][numero_dron][0])]
                #print(espera_actual)
                timeline = timeline + int(espera_actual)

            #print(timeline)
            #print(agrupacion[indice][numero_dron])
            #print(agrupacion[indice][numero_dron][3])

            #Optimo > Timeline
            if int(agrupacion[indice][numero_dron][2]) >= timeline:
                #print(timeline, agrupacion[indice][numero_dron][2])


                #Comparte intervalo
                if (len(agrupacion[indice]) > 1):
                    #Calcular si el optimo es posible
                    #print("oh no")
                    posible = 1
                    for j in range(len(agrupacion[indice])):
                        if (j == numero_dron):
                            continue
                        else:
                            lista_del = delays[int(agrupacion[indice][numero_dron][0])]
                            diferencia = int(agrupacion[indice][numero_dron][2])
                            #print(j)
                            #print(agrupacion[indice])
                            diferencia += int(lista_del[int(agrupacion[indice][j][0])])
                            
                            if (int(drones[int(agrupacion[indice][j][0])][3]) - diferencia < 0):
                                posible = 0
                            #print(diferencia)

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
            #print("ultimo")
            #print(numero_dron)
            #print("indice", indice)
            #print(agrupacion[indice])
            res = [agrupacion[indice][0][0], timeline]
            resultado.append(res)
            suma += abs(int(agrupacion[indice][0][2]) - timeline)

            agregados +=1

    #[[ndron, tiempo], costo]
    resultado.append(suma)
    print(resultado)
    


    

    #> Aplicar logica similar a la anterior:
    #Selecciono uno del grupo al azar, veo si lo puedo mandar en el optimo sin matar al resto del grupo, lo añado en tiempo x (aqui hay que pensar un par de cosas)
    #Una vez termino el grupo, siguiente grupo

    #####

    #print(drones)
    #[[ndron, tiempo], costo]
    #resultado.append(suma)
    #print(resultado)
    print(agregados)
    return resultado





####
#Main
####


#greedy_det(test1)
seed = 1
for i in range(5):  
    greedy_estoc(test3, i)