import requests
import os
import dotenv
#from deepl_translation_fun import trasnlator

BASE_DIR = os.getcwd() #method tells us the location of current working directory

# Add .env variables anywhere before SECRET_KEY
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(f"{BASE_DIR}/.env"):
    dotenv.load_dotenv(dotenv_file)
    # Update secret key
    deepl_auth_key = os.environ['auth_key'] # Instead of your actual Auth Key

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
def translator(text, language) :
    try:
        a= text.strip().encode('utf-8')
        data = f'auth_key={auth_key}&text={a}&target_lang={language}'

        response = requests.post('https://api.deepl.com/v2/translate', headers=headers, data=data)
        #print( response.json()["translations"]["text"])

        return " ".join(response.json()["translations"][0]["text"].split(" ")[1:])
    except Exception as e :
        print(e)
        return text