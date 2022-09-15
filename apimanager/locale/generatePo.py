from deepl_translation_fun import translator # Convert one language to another
from concurrent.futures import ThreadPoolExecutor as tpe # Multithreading
from threading import Lock # Locking Purpose

lock=Lock() # Intializing Lock
languages=['de','es','fr','hi'] # Defining languages
# This class is used for converting languages
class clsTranslate():
    def translateText(self, strString, strTolang):
        """
        This function translates one language into another language. It takes two
        parameters
        1. strString :=> String that you want to convert
        2. strTolang :=> Languages(fr,hi,es etc)
        """
        self.strString = strString
        self.strTolang = strTolang
        translator = translator(text=self.strString, language=self.strTolang)

        return (str(translator))

# This is method for writing file

def writeFile(language):
    print(language,"Started")
    fileName=f'locale/{language}/LC_MESSAGES/django.po' # Openning a file
    try:
        with open(fileName,encoding='utf-8') as f: # Reading from the file
            a=[i.replace("\n","") for i in f.readlines()] # Reading everyline from a file and store it into a
    except Exception as e: # same like try block. 
        print(fileName, e)
    b=0
    for i in range(len(a)):
        if 'msgid' in a[i] and a[i]!='msgid ""':
            b=i
            break

    if b!=0:
        trans=clsTranslate() # Creating object for translation class
        for i in range(b-1,len(a)):
            try:
                if "msgid" in a[i]:
                    msgid,msgstr=a[i],a[i+1]
                    if msgstr == 'msgstr ""':
                        ms=msgid[7:len(msgid)-1]
                        val=trans.translateText(ms,language)
                        a[i+1]=f'msgstr "{val}"'
                # print(a[i])
            except: pass
        try:
            lock.acquire()
            with open(fileName,'w',encoding='utf-8') as f:
                for i in a:
                    f.write(f"{i}\n")
            print(language,"is completed")
            lock.release()
        except Exception as e:
            print(e)
            lock.release()
    else:
        print(language,"is completed")

with tpe() as e:
    e.map(writeFile,languages)
