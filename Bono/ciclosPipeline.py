import re,math
Registros = {"$zero":0,"$0":0,"$at":0,"$v0":0,"$v1":0,"$a0":0,"$a1":0,"$a2":0,"$a3":0,"$t0":0,"$t1":0,"$t2":0,
                  "$t3":0,"$t4":0,"$t5":0,"$t6":0,"$t7":0,"$s0":0,"$s1":0,"$s2":0,"$s3":0,"$s4":0,"$s5":0,"$s6":0,
                  "$s7":0,"$t8":0,"$t9":0,"$gp":0,"$sp":0,"$fp":0,"$ra":0}

archMips = []
def separarArchivo():
    tmp=[]
    txtFile = open ("mipsTry.txt","r+")
    for linea in txtFile:
        tmp=re.split(', | |\n',linea)
        #print(tmp)
        archMips.append(tmp)            
        
def ciclosPipeline():
    contCiclos=4
    #flagCiclo=0
    brak=0
    while brak <(len(archMips)):
        if (archMips[brak][0]=='beq'):
            contCiclos=contCiclos+1
            label=archMips[brak][3]
            if (Registros.get(archMips[brak][1])==Registros.get(archMips[brak][2])):
                for i in range (len(archMips)):
                    if (archMips[i][0]==label):
                        contCiclos=contCiclos+1
                        brak=i
        elif (archMips[brak][0]=='bne'):
            contCiclos=contCiclos+1
            label=archMips[brak][3]
            if (Registros.get(archMips[brak][1])!=Registros.get(archMips[brak][2])):
                #rint("t1: ",Registros.get(archMips[brak][1]),"t2: ",Registros.get(archMips[brak][2]))
                for i in range (len(archMips)):
                    if (archMips[i][0]==label):
                        contCiclos=contCiclos+1
                        brak=i
            
        elif (archMips[brak][0]=='addi' or archMips[brak][0]=='addiu'):
            suma=int(Registros.get(archMips[brak][2]))+int(archMips[brak][3])
            Registros.update({archMips[brak][1]:suma})
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='add' or archMips[brak][0]=='addu'):
            suma=int(Registros.get(archMips[brak][2]))+int(Registros.get(archMips[brak][3]))
            Registros.update({archMips[brak][1]:suma})
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='sub' or archMips[brak][0]=='subu'):
            resta=int(Registros.get(archMips[brak][2]))-int(Registros.get(archMips[brak][3]))
            Registros.update({archMips[brak][1]:resta})
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='multu' or archMips[brak][0]=="mul"):
            mult=int(Registros.get(archMips[brak][2]))*int(Registros.get(archMips[brak][3]))
            Registros.update({archMips[brak][1]:mult})
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='lui'):
            Registros.update({archMips[brak][1]:archMips[brak][2]})
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='ori'):
            ori=(int(Registros.get(archMips[brak][2]),16)) | (int(archMips[brak][3],16))  #| es Or en binario
            Registros.update({archMips[brak][1]:ori})
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='or'):
            ori=(int(Registros.get(archMips[brak][2]),16)) | (int(Registros.get(archMips[brak][3]),16))  #| es Or en binario
            Registros.update({archMips[brak][1]:ori})
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='andi'):
            andi=(int(Registros.get(archMips[brak][2]),16)) & (int(archMips[brak][3],16)) #& es And en binario
            Registros.update({archMips[brak][1]:andi})
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='and'):
            andi=(int(Registros.get(archMips[brak][2]),16)) & (int(Registros.get(archMips[brak][3]),16)) #& es And en binario
            Registros.update({archMips[brak][1]:andi})
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='xori'):
            xori=(int(Registros.get(archMips[brak][2]),16)) ^ (int(archMips[brak][3],16)) #^ es Xor en binario
            Registros.update({archMips[brak][1]:xori})
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='xor'):
            xori=(int(Registros.get(archMips[brak][2]),16)) ^ (int(Registros.get(archMips[brak][3]),16)) #^ es Xor en binario
            Registros.update({archMips[brak][1]:xori})
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='nor'):
            nori=~(int(Registros.get(archMips[brak][2]),16)) & (int(archMips[brak][3],16)) #~ es not en binario
            Registros.update({archMips[brak][1]:nori})
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='j'):
            contCiclos=contCiclos+2
            label=archMips[brak][1]
            for i in range (len(archMips)):
                    if (archMips[i][0]==label):
                        brak=i
        elif (archMips[brak][0]=='jr'):
            contCiclos=contCiclos+2
        elif (archMips[brak][0]=='sw'):
            #Memoria, no se como tratarla para actualizar los registros.
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='lw'):
            #Memoria, no se como tratarla para actualizar los registros.
            contCiclos=contCiclos+1
            if (len(archMips[brak+1])>3):
                if (archMips[brak+1][0]=='sw' and archMips[brak][1]==archMips[brak+1][1]):
                    contCiclos=contCiclos+1
                elif (archMips[brak][1]==archMips[brak+1][3] or archMips[brak][1]==archMips[brak+1][2]):
                    contCiclos=contCiclos+1
            else:
                if (archMips[brak+2][0]=='sw' and archMips[brak][1]==archMips[brak+2][1]):
                    contCiclos=contCiclos+1
                elif (archMips[brak][1]==archMips[brak+2][3] or archMips[brak][1]==archMips[brak+2][2]):
                    contCiclos=contCiclos+1
        elif (archMips[brak][0]=='sll'):
            slli=(int(Registros.get(archMips[brak][2])))*(2**(int(archMips[brak][3])))
            Registros.update({archMips[brak][1]:slli})
            contCiclos=contCiclos+1
        elif (archMips[brak][0]=='slt'):
            slti=(int(Registros.get(archMips[brak][2])))/(2**(int(archMips[brak][3])))
            Registros.update({archMips[brak][1]:slti})
            contCiclos=contCiclos+1
        brak=brak+1    
    return contCiclos

    
    

separarArchivo()    
#print(archMips)
print("CRP: ",ciclosPipeline())

