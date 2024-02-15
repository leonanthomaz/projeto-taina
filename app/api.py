import googlesearch
import wikipedia
import webbrowser
import pywhatkit
from googletrans import Translator
from utils import extract_domain

"""
Classe responsável por chamar e tratar as API's do sistema. São eles: GoogleSearch, Wikipedia,
Google Tradutor e mecanismos de pesquisa no navegador.
"""

class APIHandler:
    @staticmethod
    def youtube_search(query):
        try:
            url = 'https://www.youtube.com/results?search_query=' + query
            webbrowser.get().open(url)
            print(f'url: {url}')
            return f'Pesquisa realizada no YouTube para: {query}'
        except Exception as e:
            print(f"Erro ao realizar pesquisa no YouTube: {e}")
            return "Desculpe, ocorreu um erro ao buscar no YouTube."
    @staticmethod
    def play_music(song_name):
        try:
            pywhatkit.playonyt(song_name)
            return f'Tocando música: {song_name}'
        except Exception as e:
            print(f"Erro ao reproduzir música: {e}")
            return "Desculpe, ocorreu um erro ao reproduzir a música."
    @staticmethod
    def google_search(query):
        try:
            results = googlesearch.search(query, lang='pt', num_results=1)
            for result in results:
                domain = extract_domain(result)
                return f'Achei esse resultado: {domain}'
        except Exception as e:
            print(f"Erro ao realizar pesquisa no Google: {e}")
            return []

    @staticmethod
    def wikipedia_search(query):
        try:
            wikipedia.set_lang('pt')
            result = wikipedia.summary(query)
            return result
        except wikipedia.exceptions.PageError:
            return "Desculpe, não encontrei informações sobre isso na Wikipedia."
        except wikipedia.exceptions.HTTPTimeoutError as e:
            return f"Erro: {e}"
        except Exception as e:
            print(f"Erro ao realizar pesquisa na Wikipedia: {e}")
            return None
    @staticmethod
    def translate(text):
        try:
            translator = Translator()
            translated_text = translator.translate(text, src='pt', dest='en')
            return translated_text.text
        except Exception as e:
            print(f"Erro ao traduzir texto: {e}")
            return "Desculpe, ocorreu um erro ao traduzir o texto."
