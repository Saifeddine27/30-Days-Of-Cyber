import time
import os
import subprocess
import logging

# --- CONFIGURATION ---
CHEMIN_LOG = "/var/log/auth.log"
FICHIER_MARQUE_PAGE = "bookmark.txt"
FICHIER_WHITELIST = "whitelist.txt"
FICHIER_LOG_OUTIL = "ssh_bf_detector.log"

logging.basicConfig(
    filename=FICHIER_LOG_OUTIL,
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Variables globales 
liste_blanche = set()
ips_bloquees = dict()
historique_ip = dict() # Dictionnaire pour stocker les listes de temps : { "IP": [temps1, temps2, ...] }


# --- FONCTIONS OUTILS ---

def charger_liste_blanche():
    ip_autorisees = set()
    if os.path.exists(FICHIER_WHITELIST):
        with open(FICHIER_WHITELIST, "r") as f:
            for ligne in f:
                ip_propre = ligne.strip()
                if ip_propre:
                    ip_autorisees.add(ip_propre)
        print(f"Liste blanche chargée : {len(ip_autorisees)} IP protégées.")
    else:
        print("Aucun fichier whitelist.txt trouvé. Aucune IP n'est protégée.")
    return ip_autorisees

def lire_marque_page():
    if os.path.exists(FICHIER_MARQUE_PAGE):
        with open(FICHIER_MARQUE_PAGE, "r") as f:
            contenu = f.read().strip()
            if contenu:
                return int(contenu)
    return None

def sauver_marque_page(position):
    with open(FICHIER_MARQUE_PAGE, "w") as f:
        f.write(str(position))

def bloquer_ip(ip):
    print(f"ALERTE : Attaque par Force Brute confirmée depuis {ip} .")
    logging.warning(f"Attaque par Force Brute confirmée depuis l'IP : {ip}")
    
    commande = ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
    
    try:
        subprocess.run(commande, check=True)
        print(f"SUCCÈS : L'IP {ip} a été bloquée par le pare-feu.")
        logging.info(f"Action pare-feu : L'IP {ip} a été bloquée (DROP).")
        ips_bloquees[ip] = time.time()
    except subprocess.CalledProcessError:
        print(f"ERREUR : Impossible de bloquer l'IP {ip} (As-tu lancé le script avec sudo ?)")
        logging.error(f"Échec de l'exécution iptables pour l'IP {ip}.")

def debloquer_ip(ip):
    commande = ["iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"]
    
    try:
        subprocess.run(commande, check=True)
        print(f"SUCCÈS : L'IP {ip} a purgé sa peine de 24h, elle est débloquée.")
        logging.info(f"SUCCÈS : L'IP {ip} a purgé sa peine de 24h, elle est débloquée.")
        del ips_bloquees[ip]
    except subprocess.CalledProcessError:
        print(f"ERREUR : Impossible de debloquer l'IP {ip} (As-tu lancé le script avec sudo ?)")
        logging.error(f"Échec de l'exécution iptables pour l'IP {ip}.")

# --- FONCTION PRINCIPALE ---

def ssh_bf_detector():
    global liste_blanche
    liste_blanche = charger_liste_blanche()
    
    print("Démarrage du détecteur SSH Brute Force...")
    
    # Boucle Principale (Indestructible)
    while True:
        if not os.path.exists(CHEMIN_LOG):
            time.sleep(5)
            continue
            
        taille_actuelle = os.path.getsize(CHEMIN_LOG)
        position = lire_marque_page()
        
        with open(CHEMIN_LOG, "r") as f:
            
            # Gestion du placement du curseur
            if position is not None and position <= taille_actuelle:
                print(f"Reprise de la lecture à l'octet {position}...")
                f.seek(position)
            else:
                print("Nouveau départ, on va à la fin du fichier...")
                f.seek(0, os.SEEK_END)
            
            # Boucle Secondaire (Lecture en continu)
            while True:
                ligne = f.readline()
                
                if not ligne:
                    sauver_marque_page(f.tell())
                    
                    # Vérification de la rotation des logs
                    if os.path.getsize(CHEMIN_LOG) < taille_actuelle:
                        print("\nRotation des logs détectée, réouverture du fichier...")
                        sauver_marque_page(0)
                        break
                        
                    time.sleep(0.1) 
                    for ip_bloque, temps in list(ips_bloquees.items()):
                        now = time.time()
                        if now - temps > 24*60*60:
                            debloquer_ip(ip_bloque)
                    continue    

                # --- TRAITEMENT DE LA LIGNE ---
                ligne_propre = ligne.strip()
                L = ligne_propre.split()
                
                if len(L) > 5 and L[2][0:4] == "sshd" and L[3] == "Failed" and L[4] == "password":
                    ip_ssh = L[-4]
                    if ip_ssh in liste_blanche or ip_ssh in ips_bloquees:
                        continue 
                        
                    maintenant = time.time()
                    
                    if ip_ssh in historique_ip:
                        historique_ip[ip_ssh].append(maintenant)
                    else:
                        historique_ip[ip_ssh] = [maintenant]
                        
                    # Nettoyage : On ne garde que les attaques des 10 dernières minutes (600 secondes)
                    historique_ip[ip_ssh] = [temps for temps in historique_ip[ip_ssh] if temps > maintenant - 600]
                    
                    # Sanction : S'il reste 5 attaques ou plus dans la liste
                    if len(historique_ip[ip_ssh]) >= 5:
                        bloquer_ip(ip_ssh)
                        del historique_ip[ip_ssh]


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("ATTENTION : Ce script doit être lancé en tant que root (sudo) pour pouvoir utiliser iptables.")
    
    ssh_bf_detector()