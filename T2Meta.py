test3 = "t2_Deimos.txt"
test2 = "t2_Europa.txt"
test1 = "t2_Titan.txt"

import linecache as lc

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

    drones.sort(reverse=True, key = lambda x: x[3])

    for i in range(len(drones)):
        temp = drones[i]
        temp = temp.split(" ")
        drones[i] = temp
    for i in range(len(delays)):
        temp = delays[i]
        temp = temp.split(" ")
        delays[i] = temp

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





def greedy_estoc(test):

    contar_term = {}

    agregados = 0
    timeline = 0
    resultado = []
    suma = 0

    drones, delays, tot = lectura(test)
    drones.sort(reverse=True, key = lambda x: x[3])

    for i in range(len(drones)):
        temp = drones[i]
        temp = temp.split(" ")
        drones[i] = temp
    for i in range(len(delays)):
        temp = delays[i]
        temp = temp.split(" ")
        delays[i] = temp

    for i in range(tot):

        if (drones[i][3] not in contar_term.keys()):
            contar_term[drones[i][3]] = 1
        else:
            contar_term[drones[i][3]] += 1

    #print(contar_term)
    #print(len(contar_term.keys()))


    #####
    #aqui el algoritmo
    for i in range(len(drones)):
        temp = int(drones[i][3])

        temp = int(temp/20)

        temp = temp*20
        drones[i][3] = temp

    #> Agrupar los datos segun su termino

    #> Aplicar logica similar a la anterior:
    #Selecciono uno del grupo al azar, veo si lo puedo mandar en el optimo sin matar al resto del grupo, lo añado en tiempo x (aqui hay que pensar un par de cosas)
    #Una vez termino el grupo, siguiente grupo

    #####

    print(drones)
    #[[ndron, tiempo], costo]
    #resultado.append(suma)
    #print(resultado)
    #print(agregados)
    return resultado





####
#Main
####


#greedy_det(test3)

greedy_estoc(test1)