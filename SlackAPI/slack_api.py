import os
import time
import wikipedia
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration
SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
CHANNEL_GENERAL_ID = os.environ.get("CHANNEL_GENERAL_ID")
CHANNEL_GROUP7_ID = os.environ.get("CHANNEL_GROUP7_ID")
GROUP_NAME = os.environ.get("GROUP_NAME")

# Vérification des variables requises
REQUIRED_VARS = {
    "SLACK_BOT_TOKEN": SLACK_TOKEN,
    "CHANNEL_GENERAL_ID": CHANNEL_GENERAL_ID,
    "CHANNEL_GROUP7_ID": CHANNEL_GROUP7_ID
}

missing_vars = [var for var, value in REQUIRED_VARS.items() if not value]

if missing_vars:
    print("❌ ERREUR: Variables d'environnement manquantes!")
    print(f"   Variables manquantes: {', '.join(missing_vars)}")
    print("\n💡 Solution:")
    print("   1. Vérifiez que le fichier .env existe")
    print("   2. Exécutez ./setup.sh pour configurer l'environnement")
    print("   3. Ou créez manuellement un fichier .env avec:")
    print("      SLACK_BOT_TOKEN=xoxb-...")
    print("      CHANNEL_GENERAL_ID=C...")
    print("      CHANNEL_GROUP7_ID=C...")
    print("      GROUP_NAME=Group 7")
    exit(1)

# Vérification du token
if not SLACK_TOKEN.startswith("xoxb-"):
    print("❌ ERREUR: Token Slack invalide (doit commencer par 'xoxb-')")
    print("💡 Récupérez votre token depuis:")
    print("   https://api.slack.com/apps → Votre App → OAuth & Permissions")
    exit(1)

# Initialisation du client Slack
client = WebClient(token=SLACK_TOKEN)

# PARTIE 1: Post a simple message

def post_hello_message():
    
    print("PARTIE 1: Envoi du message Hello World")

    try:
        response = client.chat_postMessage(
            channel=CHANNEL_GROUP7_ID,
            text=f"Hello world, this is {GROUP_NAME}"
        )
        
        print(f"Message posté avec succès!\n")
        return True
    
    except Exception as e:
        print(f"Erreur inattendue: {str(e)}\n")
        return False


# PARTIE 2: Upload all images from a folder

def upload_images(folder_path, channel_id=CHANNEL_GROUP7_ID):

    print(f"PARTIE 2: Upload des images depuis '{folder_path}'")
    
    try:
        files = os.listdir(folder_path) # Lister tous les fichiers du dossier images
        
        image_extensions = ['.jpg', '.jpeg', '.png'] # Filtre pour ne garder que les formats images dans le dossier
        images = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
        
        print(f"{len(images)} image(s) trouvée(s) dans '{folder_path}'")
        
        # Upload chaque image
        success_count = 0
        error_count = 0
        
        for i, image in enumerate(images, 1):
            file_path = os.path.join(folder_path, image)
            
            try:
                print(f"   [{i}/{len(images)}] Upload de '{image}'...", end=" ")
                
                response = client.files_upload_v2(
                    channel=channel_id,
                    file=file_path,
                    title=image,
                    initial_comment=f"Image {i}/{len(images)}: {image}"
                )
                
                success_count += 1
                
            except SlackApiError as e:
                error_code = e.response["error"]
                print(f"Erreur: {error_code}")
                error_count += 1
        
        print(f"\nRésultat: {success_count} succès, {error_count} erreur(s)\n")
        return success_count > 0
        
    except Exception as e:
        print(f"Erreur inattendue: {str(e)}")
        return False


# PARTIE 3: Wikipedia bot

def wikipedia_bot(channel_id=CHANNEL_GROUP7_ID):

    print("PARTIE 3: Wikipedia Bot")
    print(f"Surveillance du canal ID: {channel_id}")
    print("Envoyez un message commençant par 'Wikipedia: <titre>' pour tester")
    
    wikipedia.set_lang("en") # Définit la langue sur anglais
    
    processed_messages = set() # Eviter de répondre plusieurs fois au même message
    
    print(f"En attente de messages...\n")

    # Boucle principale du bot
    while True:
        try:
            # Récupère les 10 derniers messages
            response = client.conversations_history(
                channel=channel_id,
                limit=10
            )
            
            messages = response['messages']
            
            for message in messages:
                # Vérifie si le message contient "Wikipedia:"
                if 'text' in message and message['text'].startswith("Wikipedia:"):
                    message_ts = message['ts']
                    
                    if message_ts not in processed_messages: # Vérifie qu'on n'a pas déjà traité ce message
                        title = message['text'].replace("Wikipedia:", "").strip() # Extrait le titre Wikipedia
                        
                        print(f"Requête reçue: '{title}'")
                        
                        try:
                            # Récupère le résumé (premier paragraphe)
                            summary = wikipedia.summary(title, sentences=3)
                            
                            # Poste la réponse dans un thread
                            client.chat_postMessage(
                                channel=channel_id,
                                text=f"📖 *{title}*\n\n{summary}",
                                thread_ts=message_ts
                            )
                            
                            print(f"Réponse envoyée pour '{title}'")
                            
                        except wikipedia.exceptions.PageError:
                            # Page non trouvée
                            client.chat_postMessage(
                                channel=channel_id,
                                text=f"Aucune page Wikipedia trouvée pour '{title}'",
                                thread_ts=message_ts
                            )
                            print(f"Page non trouvée: '{title}'")
                            
                        except Exception as e:
                            # Autre erreur
                            client.chat_postMessage(
                                channel=channel_id,
                                text=f"Erreur lors de la recherche: {str(e)}",
                                thread_ts=message_ts
                            )
                            print(f"Erreur: {str(e)}")
                        
                        processed_messages.add(message_ts) # Marque le message comme traité
            
            # Pause de 2 secondes avant la prochaine vérification
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\nBot arrêté par l'utilisateur")
            return True
        
        except Exception as e:
            print(f"Erreur inattendue: {str(e)}")
            time.sleep(5)


# FONCTION PRINCIPALE

def main():

    print("SLACK API - PROJET GROUP 7")
    
    # Test d'authentification
    try:
        auth = client.auth_test()
        print(f"\nAuthentifié en tant que: @{auth['user']}")
        print(f"Team: {auth['team']}\n")
    except Exception as e:
        print(f"\nErreur d'authentification: {e}\n")
        return
    
    # Partie 1: Hello Message
    success_part1 = post_hello_message()
    
    # Partie 2: Upload Images
    if os.path.exists("images"):
        success_part2 = upload_images("images")
    else:
        print("PARTIE 2: Dossier 'images' non trouvé")
        print("Créez un dossier 'images' et ajoutez-y des images ou modifiez le chemin dans le code")
        success_part2 = False
    
    # Partie 3: Wikipedia Bot
    
    try:
        time.sleep(3)
        wikipedia_bot()
    except KeyboardInterrupt:
        print("\nWikipedia Bot ignoré")
    
    # Résumé
    print("\nRESUME:")
    print(f"- Partie 1 (Hello Message): {'Succès' if success_part1 else 'Echec'}")
    print(f"- Partie 2 (Upload Images): {'Succès' if success_part2 else 'Ignoré'}")
    print("- Partie 3 (Wikipedia Bot): Terminé")


# EXÉCUTION

if __name__ == "__main__":
    main()