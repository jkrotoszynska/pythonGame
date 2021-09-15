import pygame
import sys
import math
import random
from pygame.locals import *
from pygame import mixer

pygame.init()

# DZWIEK
# pygame.mixer.music.load('dzwiek\Ludum Dare 38 - Track 9.wav')
# pygame.mixer.music.play(-1)

OKNO = pygame.display.set_mode((400,400))
pygame.display.set_caption('Justyna’s crazy adventures')

# TEKSTURY
KrokiPrawo = [pygame.image.load('skorki\P1.png'), pygame.image.load('skorki\P2.png'), pygame.image.load('skorki\P3.png'), pygame.image.load('skorki\P4.png'), pygame.image.load('skorki\P5.png'), pygame.image.load('skorki\P6.png'), pygame.image.load('skorki\P7.png'), pygame.image.load('skorki\P8.png')]
KrokiLewo = [pygame.image.load('skorki\L1.png'), pygame.image.load('skorki\L2.png'), pygame.image.load('skorki\L3.png'), pygame.image.load('skorki\L4.png'), pygame.image.load('skorki\L5.png'), pygame.image.load('skorki\L6.png'), pygame.image.load('skorki\L7.png'), pygame.image.load('skorki\L8.png')]
TLO = pygame.image.load('skorki\wall.png')
SKOK = [pygame.image.load('skorki\SL.png'), pygame.image.load('skorki\SP.png')]
SLODYCZE = [pygame.image.load('skorki\cukierek1.png'),pygame.image.load('skorki\cukierek2.png'),pygame.image.load('skorki\cukierek3.png')]
OGRYZEK = pygame.image.load('skorki\ogryzek.png')
IKONA = pygame.image.load('ikona.png')
pygame.display.set_icon(IKONA)

# WYGLAD MENU
TloMenu = pygame.image.load('skorki\menu.png')
CZCIONKA1 = pygame.font.SysFont("OCR A Extended", 60)
CZCIONKA2 = pygame.font.SysFont("OCR A Extended", 18)
CZCIONKA3 = pygame.font.SysFont("OCR A Extended", 30)
PRZYCISK = pygame.font.SysFont("OCR A Extended", 25)
TytulMenu = CZCIONKA1.render("HELP ME!", True, (0, 0, 0))
PodTytulMenu1 = CZCIONKA2.render("arrows to move", True, (0, 0, 0))

# PodTytulMenu2 = CZCIONKA3.render("press key to play", True, (255, 18, 0))
WYJDZ = PRZYCISK.render ("EXIT", True, (155,155,155))
KONIEC = CZCIONKA1.render("GAME OVER", True, (240, 85, 0))

# POSTAC
X = 100
Y = 350
SZER = 35 
WYSOK = 38
PUDELKO_POST= (45,45,45,45)

#ZYCIE
ZDROWIE = 3
WIDOCZNOSC = True

# PORUSZANIE
V_POS = 3
SKOK = False
LICZ_SKOK = 10
LEWA = False
PRAWA = False
KROKI = 0
POSTAWA = True

# ITEMY
X_IT = random.randint(0,376)
Y_IT = -10
SZER_IT = 24
WYSOK_IT = 24
V_IT = 2
ITEM = SLODYCZE[random.randint(0,2)]
X_OGR = random.randrange(5,370)
Y_OGR = -15
WYSOK_OGR = 24
SZER_OGR = 24
V_OGR = 1.5

#BOUNS
X_BO = random.randint(0,376)
Y_BO = -15
SZER_BO = 24
WYSOK_BO = 24
V_BO = 2
BOUNS = pygame.image.load('skorki\plus.png')

#USTAWIENIA
MENU = True
CZARNY = (0,0,0)
BIALY = (255,255,255)

#REKORDY
PUNKTY = 0

def PRZYCISKI(tekst, x, y, sz, w, kol1, kol2, WYDARZENIE):
    MYSZ = pygame.mouse.get_pos()
    KLIK = pygame.mouse.get_pressed()
    MENU = True
    if x+sz > MYSZ[0] > x and  y+w > MYSZ[1] >y :
        pygame.draw.rect(OKNO, kol1, (x,y,sz,w))
        if KLIK[0] == 1 and WYDARZENIE != None:
            if WYDARZENIE == "WYJDZ":
                pygame.quit()
                quit()

    else:
        pygame.draw.rect(OKNO, kol2, (x,y,sz,w)) 
        
    OKNO.blit(WYJDZ, (170,310))
    

def POSTAC():
    global KROKI
    OKNO.blit(TLO , (0,0))
    if WIDOCZNOSC == True:
        if KROKI + 1 >= 20:
            KROKI = 0
        
        if not(POSTAWA):
            if LEWA:
                OKNO.blit(KrokiLewo[KROKI//4], (round(X),round(Y)))
                KROKI +=1
            elif PRAWA:
                OKNO.blit(KrokiPrawo[KROKI//4], (round(X),round(Y)))
                KROKI +=1
        else:
            if PRAWA:
                OKNO.blit(KrokiPrawo[0], (round(X),round(Y)))
            else:
                OKNO.blit(KrokiLewo[0], (round(X),round(Y)))

        pygame.draw.rect(OKNO, (255,0,0), (275, 6, 120, 20))
        pygame.draw.rect(OKNO, (0,255,0), (275, 6, 120 - (40*(3-ZDROWIE)), 20))

        pygame.display.update()

def ITEMS(X_IT, Y_IT, SZER_IT, WYSOK_IT, ITEM):
    OKNO.blit(ITEM, [round(X_IT), round(Y_IT), SZER_IT, WYSOK_IT])
    pygame.display.update()

def UJEMNE(X_OGR, Y_OGR, SZER_OGR, WYSOK_OGR, OGRYZEK):
    OKNO.blit(OGRYZEK, [round(X_OGR), round(Y_OGR), SZER_OGR, WYSOK_OGR])
    pygame.display.update()

def BONUSY(X_BO, Y_BO, SZER_BO, WYSOK_BO, BOUNS):
    OKNO.blit(BOUNS, [round(X_BO), round(Y_BO), SZER_BO, WYSOK_BO])
    pygame.display.update()

def PUNKTACJA(LICZ):
    TEXT = CZCIONKA3.render("POINTS:"+ str(LICZ), True, (0,0,0))
    OKNO.blit(TEXT, (0,0))
    


while True :
    pygame.time.delay(10)
    while MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    MENU = False 

        OKNO.blit(TloMenu,(0,0))
        OKNO.blit(TytulMenu, (67,100))
        OKNO.blit(PodTytulMenu1, (128,160))

        PRZYCISKI(WYJDZ,100,300,200,50,BIALY,CZARNY,"WYJDZ")
  
        pygame.display.update()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    MENU = True
    keys = pygame.key.get_pressed()
    

    if keys[pygame.K_LEFT] and X > V_POS:
        X-=V_POS
        LEWA = True
        PRAWA = False
        POSTAWA = False
    elif keys[pygame.K_RIGHT] and X < 400 - SZER - V_POS:
        X+=V_POS
        LEWA = False
        PRAWA = True
        POSTAWA = False
    else:
        POSTAWA = True
        KROKI = 0
    
    if not(SKOK):
        if keys[pygame.K_UP]:
            SKOK = True
            PRAWA = False
            LEWA = False
            KROKI = 0
    else:
        if LICZ_SKOK >= -10:
            n = 1
            if LICZ_SKOK < 0:
                n = -1
            Y -= (LICZ_SKOK ** 2) * 0.5 * n
            LICZ_SKOK -= 1
        else:
            SKOK = False
            LICZ_SKOK = 10
    
    POSTAC()
    ITEMS(X_IT, Y_IT, SZER_IT, WYSOK_IT, ITEM)
    Y_IT += V_IT
    PUNKTACJA(PUNKTY)
    UJEMNE(X_OGR, Y_OGR, SZER_OGR, WYSOK_OGR, OGRYZEK)
    Y_OGR += V_OGR
    BONUSY(X_BO, Y_BO, SZER_BO, WYSOK_BO, BOUNS)
    Y_BO += V_BO
    pygame.display.update()

    ODLEGLOSC = math.sqrt(math.pow(X-X_IT+6, 2)+ math.pow(Y-Y_IT+6,2))
    if ODLEGLOSC < 15:
        PUNKTY+=1
        Y_IT = -10
        X_IT = random.randrange(0,376)
        ITEM = SLODYCZE[random.randint(0,2)]

    ODLEGLOSC = math.sqrt(math.pow(X-X_OGR+6, 2)+ math.pow(Y-Y_OGR+6,2))
    if ODLEGLOSC < 10:
        PUNKTY-=5
        Y_OGR = -10
        X_OGR = random.randrange(0,376)

    ODLEGLOSC = math.sqrt(math.pow(X-X_BO+6, 2)+ math.pow(Y-Y_BO+6,2))
    if ODLEGLOSC < 10:
        PUNKTY+=15
        Y_BO = -20
        X_BO = random.randrange(0,376)

    if Y_IT > 400:
        Y_IT = 0 - WYSOK_IT
        X_IT = random.randrange(0,376)
        ITEM = SLODYCZE[random.randint(0,2)]
        V_IT+=0.05
        if ZDROWIE > 0:
            ZDROWIE -=1

    if Y_OGR > 400:
        Y_OGR = 0 - WYSOK_OGR
        X_OGR = random.randrange(0,376)
        V_OGR+=0.06
    
    if Y_BO > 400:
        Y_BO = 0 - WYSOK_BO
        X_BO = random.randrange(0,376)
        V_BO+=0.08

        while ZDROWIE<1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            OKNO.blit(TloMenu,(0,0))
            OKNO.blit(KONIEC, (42,100))
            TEXT = CZCIONKA3.render("POINTS:"+ str(PUNKTY), True, (0,0,0))
            OKNO.blit(TEXT, (118,160))
            PRZYCISKI(WYJDZ,100,300,200,50,BIALY,CZARNY,"WYJDZ")
  
            pygame.display.update()
