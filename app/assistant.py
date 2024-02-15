
from engine import Engine

engine = Engine()

"""
A classe Taina é responsável por guardar os nomes da assistente e geração do nome de usuário, onde
captura o nome em um determinado arquivo e guarda para futuros processos.
"""

class Taina:
    def __init__(self):
        self.assist_name = "Tainá"
        self.person = self.load_person_name()

    def load_person_name(self):
        """
        Carrega o nome da pessoa do arquivo se disponível, caso contrário, pergunta e salva no arquivo.
        """
        try:
            with open("config/person_name.txt", "r") as file:
                person_name = file.read().strip()
                if person_name:
                    return person_name
        except ValueError:
            engine.engine_record_audio(f'Não entendi seu nome, pode repetir?')
            return
        except FileNotFoundError:
            print('Falha ao processar arquivo de configuração...')
            pass

        engine.engine_record_audio(f'Olá! Sou {self.assist_name}. Qual é o seu nome?')
        person_name = engine.voice_data.capitalize()

        with open("config/person_name.txt", "w") as file:
            file.write(person_name)
        return person_name
