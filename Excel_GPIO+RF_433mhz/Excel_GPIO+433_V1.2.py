#Excel_GPIO+433 mhz/horaire v1.2 06/02/2017

import RPi.GPIO as GPIO                       #GPIO
import time                                   #Heure
from datetime import date                     #Date
import calendar                               #Jour de la semmaine
import xlrd                                   #Lecture fichier Excel
from pi_switch import RCSwitchSender          #Radio
from apscheduler.scheduler import Scheduler   #Relence le programme
from ConfigParser import SafeConfigParser     #Ficher de configuration


#Configuration RF 433 mhz
sender = RCSwitchSender()
sender.enableTransmit(0)#pin de transmision (wripi)

#Configuration Sortie GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)
GPIO.output(25,GPIO.LOW)

# Lancez Parser et lisez le fichier de configuration
parser = SafeConfigParser()                       

#code transmie par radio
code_on = 12
code_off = 11

#declaration de variable
sortie = False


   
###############################################################################################
#                                   Fonction principale                                       #
###############################################################################################
def main ():
    
    #lecture du fichier configuration
    parser.read('Configuration.cfg')
    out = parser.get('sortie', 'out')#Type de sortie
    fichier = parser.get('Doc', 'fichier')#adresse de fichier excel
    
    
    
    Ma_date = date.today()#récuperation de la date du system
    #print Ma_date
    Mon_heure = time.strftime("%H%M", time.localtime(time.time()))#récuperation de l'heure du system
    #print Mon_heure
    Jour = calendar.day_name[Ma_date.weekday()]#recuperation du jour du system
    #print jour
    
    
    
    #ouverture du classeur
    classeur = xlrd.open_workbook(fichier)
    #Récuperation du nom de toutes les feuilles sous forme de liste
    nom_des_feuilles = classeur.sheet_names()
    #Récupération de la première feuille
    feuille = classeur.sheet_by_name(nom_des_feuilles[0])
    
  
    if Jour == 'Monday':
        if (feuille.cell_value(1,1) <= Mon_heure) and (feuille.cell_value(2,1) > Mon_heure):
            sortie = True
        else:
            sortie = False
            
    if Jour == 'Tuesday':
        if (feuille.cell_value(1,2) <= Mon_heure) and (feuille.cell_value(2,2) > Mon_heure):
            sortie = True
        else:
            sortie = False
    
    if Jour == 'Wednesday':
        if (feuille.cell_value(1,3) <= Mon_heure) and (feuille.cell_value(2,3) > Mon_heure):
            sortie = True
        else:
            sortie = False
    
    if Jour == 'Thursday':
        if (feuille.cell_value(1,4) <= Mon_heure) and (feuille.cell_value(2,4) > Mon_heure):
            sortie = True
        else:
            sortie = False
    
    if Jour == 'Friday':
        if (feuille.cell_value(1,5) <= Mon_heure) and (feuille.cell_value(2,5) > Mon_heure):
            sortie = True
        else:
            sortie = False
    
    if Jour == 'Saturday':
        if (feuille.cell_value(1,6) <= Mon_heure) and (feuille.cell_value(2,6) > Mon_heure):
            sortie = True
        else:
            sortie = False
    
    if Jour == 'Sunday':
        if (feuille.cell_value(1,7) <= Mon_heure) and (feuille.cell_value(2,7) > Mon_heure):
            sortie = True
        else:
            sortie = False
    
    print sortie
    
    if sortie == True and out == '433':
        print "433"
        sender.sendDecimal(code_on, 24)
    else:
        sender.sendDecimal(code_off, 24)
        
        
    if sortie == True and out == 'GPIO':
        print "GPIO"
        GPIO.output(25,GPIO.HIGH)
    else:
        GPIO.output(25,GPIO.LOW)
    
###############################################################################################
#            Fonction qui relance la lecture du fichier tout les 10 seconds                   #
###############################################################################################
def callable_func():
   
    print "----------------------------"
    main()
    print "----------------------------"


sched = Scheduler(standalone=True)
sched.add_interval_job(callable_func,seconds=10)
sched.start()


