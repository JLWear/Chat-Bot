import time
import requests
from config import CLIENT_ID, CLIENT_SECRET

# Dictionnaire local des métiers par centre d’intérêt
local_metiers = {
    "sport": [
        {
            "code": "G1204",
            "libelle": "Éducateur sportif",
            "description": (
                "L’éducateur sportif enseigne et encadre la pratique d’activités physiques et sportives. "
                "Il prépare des séances adaptées au public et veille à la sécurité des pratiquants.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/educateur-sportif"
            )
        },
        {
            "code": "K1206",
            "libelle": "Coach sportif",
            "description": (
                "Le coach sportif accompagne ses clients dans leurs objectifs de remise en forme ou performance. "
                "Il établit des programmes personnalisés et motive.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/coach-sportif"
            )
        },
        {
            "code": "G1203",
            "libelle": "Animateur sportif",
            "description": (
                "L’animateur sportif organise des activités sportives et de loisirs pour tous publics, "
                "dans des structures variées.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/animateur-sportif"
            )
        },
        {
            "code": "G1202",
            "libelle": "Entraîneur de sport",
            "description": (
                "L’entraîneur prépare les sportifs à la compétition, analyse les performances et planifie les entraînements.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/entraineur-sportif"
            )
        },
    ],
    "informatique": [
        {
            "code": "M1805",
            "libelle": "Développeur web",
            "description": (
                "Le développeur web conçoit, développe et maintient des sites ou applications web. "
                "Il maîtrise plusieurs langages et outils techniques.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/developpeur-web"
            )
        },
        {
            "code": "M1801",
            "libelle": "Technicien support informatique",
            "description": (
                "Le technicien support informatique assiste les utilisateurs et intervient pour résoudre les problèmes techniques.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/technicien-support-informatique"
            )
        },
        {
            "code": "M1802",
            "libelle": "Analyste programmeur",
            "description": (
                "L’analyste programmeur conçoit des programmes informatiques en fonction des besoins exprimés, "
                "développe et teste les logiciels.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/analyste-programmeur"
            )
        },
    ],
    "nature": [
        {
            "code": "A1203",
            "libelle": "Jardinier paysagiste",
            "description": (
                "Le jardinier paysagiste conçoit, crée et entretient des espaces verts, jardins, et parcs.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/jardinier-paysagiste"
            )
        },
        {
            "code": "A1301",
            "libelle": "Agent d'entretien des espaces naturels",
            "description": (
                "L’agent d’entretien des espaces naturels protège, restaure et maintient les milieux naturels.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/agent-dentretien-des-espaces-naturels"
            )
        },
    ],
    "animaux": [
        {
            "code": "A1503",
            "libelle": "Soigneur animalier",
            "description": (
                "Le soigneur animalier assure le bien-être, la santé et la nourriture des animaux en captivité.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/soigneur-animalier"
            )
        },
        {
            "code": "A1501",
            "libelle": "Éleveur d'animaux",
            "description": (
                "L’éleveur d’animaux élève des animaux pour la production agricole ou l’élevage de race.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/eleveur-danimaux"
            )
        },
    ],
     "art": [
        {
            "code": "E1101",
            "libelle": "Peintre décorateur",
            "description": (
                "Le peintre décorateur applique des peintures, vernis et revêtements muraux.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/peintre-decorateur"
            )
        },
        {
            "code": "E1104",
            "libelle": "Illustrateur",
            "description": (
                "L’illustrateur réalise des images pour livres, presse ou publicité.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/illustrateur"
            )
        },
    ],
    "sante": [
        {
            "code": "J1502",
            "libelle": "Infirmier",
            "description": (
                "L’infirmier assure les soins généraux et l’accompagnement des patients.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/infirmier"
            )
        },
        {
            "code": "J1503",
            "libelle": "Aide-soignant",
            "description": (
                "L’aide-soignant assiste l’infirmier et prend en charge l’hygiène et le confort du patient.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/aide-soignant"
            )
        },
    ],
    "education": [
        {
            "code": "K2104",
            "libelle": "Professeur des écoles",
            "description": (
                "Le professeur des écoles enseigne aux élèves du primaire.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/professeur-des-ecoles"
            )
        },
        {
            "code": "K2105",
            "libelle": "Éducateur spécialisé",
            "description": (
                "L’éducateur spécialisé accompagne des publics en difficulté sociale.\n"
                "En savoir plus : https://www.onisep.fr/Ressources/Univers-Metier/Metiers/educateur-specialise"
            )
        },
    ],
}


class RomeAPI:
    def __init__(self):
        self.token = None
        self.token_expiry = 0

    def authenticate(self):
        url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire"
        data = {
            "grant_type": "client_credentials",
            "scope": "api_rome-metiersv1"
        }
        resp = requests.post(
            url,
            data=data,
            auth=(CLIENT_ID, CLIENT_SECRET),
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            print(f"[AUTH ERROR {resp.status_code}] {resp.text}")
            raise

        result = resp.json()
        self.token = result["access_token"]
        self.token_expiry = time.time() + result.get("expires_in", 3600) - 60
        print("[OK] Token obtenu.")

    def get_token(self):
        if not self.token or time.time() > self.token_expiry:
            self.authenticate()
        return self.token

    def search_metiers(self, query):
        try:
            token = self.get_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            }
            params = {
                "q": query,
                "champs": "code,libelle",
                "op": "AND"
            }

            url = "https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/metier/requete"
            resp = requests.get(url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            return data.get("resultats", [])

        except requests.exceptions.HTTPError as e:
            print(f"[ERREUR API] {e}")
            print(f"[INFO] Utilisation du dictionnaire local pour : {query}")
            return local_metiers.get(query.lower(), [])

    def get_metier_detail(self, rome_code):
        try:
            token = self.get_token()
            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
            url = f"https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/metier/{rome_code}"
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()
    
        except requests.exceptions.HTTPError as e:
            print(f"[ERREUR API] {e}")
            print(f"[INFO] Utilisation du dictionnaire local pour le code : {rome_code}")
            # Recherche dans local_metiers
            for metiers in local_metiers.values():
                for metier in metiers:
                    if metier["code"] == rome_code:
                        return {
                            "code": metier["code"],
                            "libelle": metier["libelle"],
                            "description": metier.get("description", "Description non disponible.")
                        }
            # Si pas trouvé
            return {
                "code": rome_code,
                "libelle": "Métier inconnu",
                "description": "Description non disponible."
            }
