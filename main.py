from numpy import asarray
from PIL import Image

def hide(msg,image_name):
    image = Image.open(image_name)
    data = asarray(image).copy()
    
    #Convertir le message en octet
    final_message=""
    for lettre in msg:
        position_ascii = ord(lettre)
        binaire = bin(position_ascii)[2:]
        while len(binaire) < 8:
            binaire = "0" + binaire
        final_message += binaire
    print("Messsage encodé en binaire :", final_message)

    #Recupère la longueur et l'inscrit sur 2 octet (16bits)
    longueur = len(final_message)
    binaire = bin(longueur)[2:]
    while len(binaire)<16:
        binaire = "0" + binaire
    print("Taille a encoder :",binaire)
    result_message = binaire + final_message
    print('Result message',result_message)
    #data[y][x][rgb]
    print(data[0][3])
    tour=0
    y=0
    for line in data:
        x=0
        for colonne in line:
            rgb=0
            for couleur in colonne:
                valeur=data[y][x][rgb]
                binaire=bin(valeur)[2:]
                binaire_list = list(binaire)
                del binaire_list[-1]
                binaire_list.append(result_message[tour])
                decimal = int("".join(binaire_list),2)
                data[y][x][rgb]=decimal
                tour +=1
                rgb+=1
                if tour >= len(result_message):
                    break
            x+=1
            if tour >= len(result_message):
                break
        y+=1
        if tour >= len(result_message):
            break
    imagefinal = Image.fromarray(data)
    imagefinal.save("SERCRET.png")
        
def discover(image_name):
    image = Image.open(image_name)
    data = asarray(image).copy()

    tour=0
    taille=""
    message=""
    taille_new=12673
    y=0
    for line in data:
        x=0
        for colonne in line:
            rgb=0
            for color in colonne:
                valeur = data[y][x][rgb]
                binaire=bin(valeur)[2:]
                last=binaire[-1]
                if tour <16:
                    taille+=last
                if tour==16:
                    taille_new=int(taille,2)
                if tour-16 < taille_new:
                    message+=last
                if tour-16 >= taille_new:
                    break
                tour+=1
                rgb+=1
            if tour-16 >= taille_new:
                break
            x+=1
        if tour-16 >= taille_new:
            break
        y+=1
    print(message)
    octet=[]
    for i in range(len(message)//8):
        octet.append(message[i*8:(i+1)*8])
    print(octet)
    result=""
    for oct in octet:
        index=int(oct,2)
        lettre_ascii=chr(index)
        print(lettre_ascii)
        result+=lettre_ascii
    print("MESSAGE:",str(result)[2:])



hide("Abonnez vous :-)","photo.JPG")
discover("SERCRET.png")