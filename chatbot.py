from rome_api import RomeAPI
import re

class OrientationChatbot:
    def __init__(self):
        self.rome_api = RomeAPI()
        self.contexts = {}

    def create_context(self):
        context_id = "session"  # simplification, un seul user ici
        self.contexts[context_id] = {
            "stage": "ask_interest",
            "interests": None,
            "metiers": None,
            "selected_metier": None
        }
        return context_id

    def extract_name(self, user_input):
        match = re.search(r"my name is ([a-zA-Z\s]+)", user_input, re.I)
        if match:
            return match.group(1).strip()
        return None

    def process_message(self, context_id, message):
        context = self.contexts.get(context_id)
        if not context:
            return "Erreur : contexte introuvable."

        stage = context["stage"]

        if stage == "ask_interest":
            try:
                metiers = self.rome_api.search_metiers(message)
            except Exception as e:
                print(f"[ERREUR API] {e}")
                print(f"[INFO] Utilisation du dictionnaire local pour : {message.lower()}")
                from local_metiers import METIERS_PAR_INTERET
                metiers = METIERS_PAR_INTERET.get(message.lower(), [])

            if not metiers:
                return ("Aucun métier trouvé pour cet intérêt pour le moment. "
                        "Tu peux explorer plus de métiers sur le site de l’ONISEP : "
                        "https://www.onisep.fr")

            suggestions = metiers[:3]
            context["metiers"] = suggestions
            context["stage"] = "ask_job_choice"

            lines = "\n".join(f"{i+1}. {m['libelle']}" for i, m in enumerate(suggestions))
            return f"Voici quelques métiers associés :\n{lines}\nLequel t'intéresse ? (réponds par un numéro)"

        if stage == "ask_job_choice":
            try:
                index = int(message.strip()) - 1
                selected = context["metiers"][index]
            except (ValueError, IndexError):
                return "Merci de répondre avec un numéro valide (1, 2 ou 3)."

            context["selected_metier"] = selected
            context["stage"] = "show_detail"

            try:
                detail = self.rome_api.get_metier_detail(selected["code"])
                desc = detail.get("description", "Description non disponible.")
            except Exception as e:
                print(f"[ERREUR API - détail] {e}")
                desc = "Description non disponible."

            return f"Voici une fiche métier pour {selected['libelle']} :\n{desc}\nEst-ce que ce métier t'intéresse ? (oui/non)"

        if stage == "show_detail":
            if "oui" in message.lower():
                context["stage"] = "ask_continue"
                return "As-tu besoin d’aide pour un autre métier ? (oui/non)"
            elif "non" in message.lower():
                context["stage"] = "ask_interest"
                return "D'accord, quels sont alors tes autres centres d’intérêt ?"
            else:
                return "Merci de répondre par oui ou non."

        if stage == "end":
            context["stage"] = "ask_interest"
            context["interests"] = None
            context["metiers"] = None
            context["selected_metier"] = None
            return "Quels sont tes centres d’intérêt ?"
        
        if stage == "ask_continue":
            if "oui" in message.lower():
                context["stage"] = "ask_interest"
                context["interests"] = None
                context["metiers"] = None
                context["selected_metier"] = None
                return "Quels sont tes centres d’intérêt ?"
            elif "non" in message.lower():
                context["stage"] = "end"
                context["closed"] = True
                return "Très bien, n'hésite pas à revenir si tu as d'autres questions. À bientôt !"
            else:
                return "Merci de répondre par oui ou non."

        return "Je n'ai pas compris. Peux-tu reformuler ?"
