import os
import random
import webbrowser

import playsound
import speech_recognition as sr
import pyttsx3
from gtts import gTTS

from api import APIHandler
from utils import engine_check

api = APIHandler()

"""
O coração do sistema. Aqui se obtém o controle da gravação de voz, transformação de texto para fala e
de fala para texto, processamento de respostas e desligamento de sistema.
"""

class Engine:
    def __init__(self):
        self.assistant = ''
        self.person = ''
        self.greeting_exists = False
        self.get_response = False
        self.get_action = False
        self.actions = False
        self.control_system = True
        self.voice_data = ''
        
        self.engine = pyttsx3.init()
        # self.engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')
        # print(self.engine.getProperty('voice'))
        # self.engine.setProperty('rate', 150)  # Define a velocidade da voz
        # self.engine.setProperty('word_gap', 5)  # Define a pausa entre as palavras
        # self.engine.setProperty('language', 'pt-br')  # Define o idioma
        # self.engine.runAndWait()

        self.recognizer = sr.Recognizer()

    def engine_record_audio(self, ask=""):
        """
        Grava o áudio do microfone e converte em texto.
        """
        with sr.Microphone() as source:

            self.recognizer.adjust_for_ambient_noise(source)

            if ask:
                print(f'{self.assistant} está falando... 🎧')
                self.engine_speak(ask)

            audio = self.recognizer.listen(source, 8, 10)
            # print(f'{self.assistant} está processando... Aguarde 🕓')

            try:
                print(f'{self.person} está falando... 🎙️')
                self.voice_data = self.recognizer.recognize_google(audio, language='pt-BR')
                print(f'>> {self.person} diz: {self.voice_data} <<')
            except sr.UnknownValueError:
                print('Tente outro comando...')
                self.engine_speak(f'Desculpe {self.person}, Eu não entendi o que você quis dizer... Pode repetir?')
            except sr.RequestError:
                print('Tente novamente pq deu ruim...')
                self.engine_speak(f'Foi mal chefe.. Servidor indisponível')

            if not self.voice_data:
                print(f'>> {self.person} diz: nada... <<')

            self.voice_data = self.voice_data.lower()

            return self.voice_data.lower()

    def engine_speak(self, audio_string):
        """
        Fala da assistente
        """
        audio_string = str(audio_string)
        tts = gTTS(text=audio_string, lang='pt-BR', slow=False, tld='com.br', lang_check=True)
        r = random.randint(1, 3000)
        audio_file = f'audios/audio{r}.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print(f'{self.assistant} diz: {audio_string}')
        os.remove(audio_file)

    def engine_response(self, voice_data):
        """
        Responde à entrada de voz com base nas palavras-chave detectadas.
        """
        actions = {
            'saudacao': {
                'keywords': ['bom dia', 'boa tarde', 'boa noite', 'oi', 'olá', 'hello'],
                'responses': [
                    f'Fala {self.person}, tranquilo?',
                    f'Beleza, {self.person}? Como você está hoje?',
                    f'De boinha, {self.person}?',
                    f'Oi chefe {self.person}! Bom te ver de novo!',
                    f'Olá {self.person}! Estou disponível!',
                    f'Como vai, senhor? Tem algo que eu possa fazer?',
                ]
            },
            'estado': {
                'keywords': ['tô', 'estou'],
                'responses': {
                    'boa': 'Que beleza, senhor! Aguarde um instante...',
                    'bem': 'Que bom chefe! Vamos em frente! Aguarde um instante...',
                    'mal': 'Relaxa senhor, vai melhorar... Vamos prosseguir? Aguarde um instante...',
                    'pensando': 'Ok, estou aguardando...'
                }
            },
            'parar': {
                'keywords': ['parar', 'pausar', 'encerrar', 'fechar', 'acabar'],
                'responses': ['Certo, senhor...']
            },
            'continuar': {
                'keywords': ['quero continuar', 'continue', 'prossiga', 'vamos continuar'],
                'responses': ['Ok, senhor. Vamos continuar...']
            },
            'continuar_conversa': {
                'keywords': ['vamos continuar'],
                'responses': ['Pode falar, chefe...']
            },
            'desligar': {
                'keywords': ['sair', 'desligar', 'finalizar', 'cala a boca', 'ja deu', 'pode dormir'],
                'responses': ['Desligando o sistema...'],
            },
            'tocar_musica': {
                'keywords': ['toque', 'pedrada', 'hino'],
                'action': lambda song: api.play_music(song)
            },
            'acessar_site': {
                'keywords': ['site'],
                'action': lambda site: webbrowser.get().open(f'https://www.{"-".join(site.split())}.com')
            },
            'pesquisa_youtube': {
                'keywords': ['youtube', 'YouTube'],
                'action': lambda video: api.youtube_search(voice_data.split('youtube')[-1])
            },
            'pesquisa_google': {
                'keywords': ['google', 'Google'],
                'action': lambda search: api.google_search(search)
            },
            'pesquisa_wikipedia': {
                'keywords': ['wikipedia', 'Wikipédia'],
                'action': lambda word: api.wikipedia_search(word)
            },
            'traducao': {
                'keywords': ['traduza'],
                'action': lambda phrase: api.translate(phrase)
            }
        }

        for action, data in actions.items():
            if engine_check(data['keywords'], voice_data):
                if 'responses' in data:
                    if isinstance(data['responses'], list):
                        response = random.choice(data['responses'])
                    else:
                        state_response = voice_data.split(data['keywords'][0])[1].strip().lower()
                        response = data['responses'].get(state_response, 'Desculpe, não entendi.')
                    self.engine_speak(response)
                if 'action' in data:
                    if not self.actions:
                        term = voice_data.split(data['keywords'][-1])[-1].strip()  # Obtém o texto após o último keyword
                        self.engine_speak(data['action'](term))
                        self.actions = True
                    else:
                        self.engine_speak('Limpando dados de pesquisa...')
                        data.clear()
                        self.actions = False
                        return
                if action == 'saudacao':
                    self.greeting_exists = True
                if action == 'desligar':
                    self.engine_off()
                break

    def engine_process_name(self, assistant, person):
        """
        Processa o nome de usuário e da assistente
        """
        self.assistant = assistant
        self.person = person

    def engine_off(self):
        """
        Encerramento do sistema
        """
        self.control_system = False

