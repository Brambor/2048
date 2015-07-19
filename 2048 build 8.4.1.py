print("loading...")

import pygame
import sys
import math
import random
import copy

pygame.init() #potřeba zadat
screen = pygame.display.set_mode((400,425)) #vel.okna
pygame.display.set_caption("2048")#název okna
pygame.display.set_icon(pygame.image.load("pic/logo32.png"))
clock = pygame.time.Clock()

blok_img= pygame.image.load("pic/blok.png")
blok= pygame.sprite.Sprite()
blok.image= blok_img
blok.rect=blok_img.get_rect()
blok.rect.center= (200, 13)

font = pygame.font.SysFont("conzolas", 32)

obrazky = []
for i in range (18):
    obrazky.append(pygame.image.load("pic/"+str(i)+".png").convert_alpha())
    
bg_color = (204, 204, 255)

soubor = open("save.txt", "r")
save = soubor.read()
soubor.close()

pole = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    ]
if save == "":
    score, highscore = 0, 0
    x, y = 0, 0
    null = []
    for radka in pole:
        y = 0
        for ctverec in radka:
            if ctverec ==0:
                null.append((x, y))
            y += 1            
        x += 1
    x, y = random.choice (null)
    pole[x][y]= 1
else:
    prepole, score, highscore = save.split(",")
    score, highscore = int(score), int(highscore)
    prepole = list(prepole)
    i = 0
    while i < (len(prepole)-1):
        if (prepole[i] !=" ") and (prepole[i+1] !=" "):
            prepole[i] = prepole[i]+prepole[i+1]
            del prepole [i+1]
        elif prepole[i] == " ":
            del prepole[i]
            i-=1
        i+=1
    for radek in range(4):
        for sloup in range(4):
            pole[sloup][radek] = int(prepole[sloup*4 + radek])

print("press 'r' for restart") #\npress 'h' for highscore
def presyp (pole):
    
    global score
    vysledek = []
    zmeny = [[],[],[],[]] #z jakého na jaké
    
    Radek = 0
    for radka in pole:
      #Odebere nuly
        nova_radka = []
        pozice = 0
        posunuti = False
        for cislicko in radka:
            if cislicko != 0:
                nova_radka.append(cislicko)
            else:
                posunuti = True
            if posunuti and cislicko != 0:
                zmeny[Radek].append(str(pozice)+str(len(nova_radka)-1))
            pozice += 1
      #Spojí
        for index in range(4):
            if index >= len(nova_radka)-1:
                break
            if nova_radka[index] == nova_radka[index+1]:
                
                for i in range(len(zmeny[Radek])):
                    if int(list(zmeny[Radek][i])[1]) >= index + 1: # takhle ne
                        zmeny[Radek][i] = list(zmeny[Radek][i])[0] + str(int(list(zmeny[Radek][i])[1])-1)
                zmeny[Radek].append(str(index+1)+str(index))
                score += 2**(int(nova_radka[index])+1)
                del nova_radka[index]
                nova_radka[index] += 1
                #print ("score :", score)

      #Přidá nuly
        for i in range (4- len(nova_radka)):
            nova_radka.append(0)
        vysledek.append(nova_radka)
        Radek += 1
    #ANIMACE plán: nejdřív to přejede, pak se to změní, a u toho to "blikne" (o trochu se zvětší a zase zmenší už to nové pole - barva i číslo > celý obrázek)
    if pole != vysledek: 
        print(zmeny)
    return vysledek
screen.fill(bg_color)
nove_policko = None
velikost = 0

x, y = 0, 0
for radka in pole:
    y = 0
    for ctverec in radka:
        screen.blit(obrazky[pole[x][y]], (x*100, y*100+25)) #POSUN
        y += 1            
    x += 1
pygame.display.update()
while True:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            print("saving...")
            poleS = []
            for i in range(4):
                for i2 in range(4):
                    pole[i][i2] = str(pole[i][i2])
            for i in pole:
                poleS.append(" ".join(i))
            poleS = " ".join(poleS) + "," + str(score) + "," + str(highscore)
            
            soubor = open("save.txt","w")
            soubor.write(poleS)
            soubor.close()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            pole = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                ]
            score=0
            screen.fill(bg_color)
            pygame.display.update()
            #print ("RESTART\nscore :", score)
            x, y = 0, 0
            null = []
            for radka in pole:
                y = 0
                for ctverec in radka:
                    if ctverec ==0:
                        null.append((x, y))
                    y += 1            
                x += 1
            x, y = random.choice (null)
            pole[x][y]= 1
        #elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
        #    print ("highscore: ", highscore)
        elif event.type == pygame.KEYDOWN:
            
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                stare_pole = copy.copy(pole)
                if event.key == pygame.K_UP:
                    pole = presyp(pole)
                if event.key == pygame.K_RIGHT:
                    pole = list(zip(*pole[::-1]))
                 
                    pole = presyp(pole)
                    pole = list(zip(*pole[::-1]))
                    pole = list(zip(*pole[::-1]))
                    pole = list(zip(*pole[::-1]))
                    pole = [list(x) for x in pole]
                if event.key == pygame.K_DOWN:
                    pole = list(zip(*pole[::-1]))                                        
                    pole = list(zip(*pole[::-1]))
                   
                    pole = presyp(pole)
                    pole = list(zip(*pole[::-1]))
                    pole = list(zip(*pole[::-1]))
                    pole = [list(x) for x in pole]
                if event.key == pygame.K_LEFT:
                    pole = list(zip(*pole[::-1]))                                        
                    pole = list(zip(*pole[::-1]))                    
                    pole = list(zip(*pole[::-1]))
                    
                    pole = presyp(pole)
                    pole = list(zip(*pole[::-1]))
                    pole = [list(x) for x in pole]
                screen.fill(bg_color)
                x, y = 0, 0
                nuly = []
                
                for radka in pole:
                    y = 0
                    for ctverec in radka:
                        if ctverec == 0:
                            nuly.append((x, y))
                        y += 1            
                    x += 1
                if len(nuly) == 0 and stare_pole != pole: #Game over
                    sys.exit()
                if stare_pole != pole:
                    x, y = random.choice(nuly)
                    pole[x][y]=random.choice((1, 1, 1, 1, 1, 1, 1, 2)) #7:1
                    nove_policko = (x, y)
                    velikost = 0

                if highscore < score :
                    highscore = score
                
    x, y = 0, 0
    for radka in pole:
        y = 0
        for ctverec in radka:
            if nove_policko and x == nove_policko[0] and y == nove_policko[1]: ##Tohle mi nepřipadá správně
                rect = pygame.Rect(0, 0, min(100,velikost), min(100, velikost))
                rect.center = (50, 50)
                
                screen.blit(obrazky[pole[x][y]], (x*100+ max (0,(50-velikost/2)), 25+y*100+ max (0,(50-velikost/2))), rect)
            else:
                screen.blit(obrazky[pole[x][y]], (x*100, y*100+25))
            y += 1
            
        x += 1

    text = font.render(("score : "+str(score)), True,(32, 32, 32))
    text_rect = text.get_rect()
    text_rect.topleft = (18, 4)

    htext = font.render(("highscore : "+str(highscore)), True,(32, 32, 32))
    htext_rect = htext.get_rect()
    htext_rect.topleft = (176, 4)


    
    screen.blit(blok.image, blok.rect)
    screen.blit(text, text_rect)
    screen.blit(htext, htext_rect)
    
    velikost += 1
    pygame.display.update()
