from deepl_translation_function import translator # Convert one language to another
from concurrent.futures import ThreadPoolExecutor as tpe # Multithreading
from threading import Lock # Locking Purpose

lock=Lock() # Intializing Lock
languages=['de','es','fr','hi'] # Defining languages


# This class is used for converting languages
class languageConverting():
    def parametersTextConverte(self, stString, prevlangToNewlang):
        """
        This function translates one language into another language. It takes two
        parameters
        1. prevStrToNewString :=> String that you want to convert
        2. prevlangToNewlang :=> Languages(fr,hi,es etc)
        """
        self.prevStrToNewString = prevStrToNewString
        self.prevlangToNewlang = prevlangToNewlang
        translator = translator(text=self.prevStrToNewString, language=self.prevlangToNewlang)

        return (str(translator))
# This is method for writing file

def localeWriteFile(language):
    fileName=f'locale/{language}/LC_MESSAGES/django.po' # Openning a file
    try:
        with open(fileName,encoding='utf-8') as f: # Reading from the file
            a=[i.replace("\n","") for i in f.readlines()] # Reading everyline from a file and store it into a
    except Exception as e: # same like try block. 
    b=0
    for i in range(len(a)):
        if 'msgid' in a[i] and a[i]!='msgid ""':
            b=i
            break

    if b!=0:
        trans=languageConverting() # Creating object for translation class
        for i in range(b-1,len(a)):
            try:
                if "msgid" in a[i]:
                    msgid,msgstr=a[i],a[i+1]
                    if msgstr == 'msgstr ""':
                        ms=msgid[7:len(msgid)-1]
                        val=trans.parametersTextConverte(ms,language)
                        a[i+1]=f'msgstr "{val}"'
            except: pass
        try:
            lock.acquire()
            with open(fileName,'w',encoding='utf-8') as f:
                for i in a:
                    f.write(f"{i}\n")
            lock.release()
        except Exception as e:
            lock.release()
    else:

with tpe() as e:
    e.map(localeWriteFile,languages)
