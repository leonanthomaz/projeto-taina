
import utils
from assistant import Taina
from engine import Engine
import threading

# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.debug('Iniciando o serviço...')

assistant = Taina()
engine = Engine()


"""
Arquivo principal do projeto. A função handle_audio_input carrega os nomes do assistente e do usuario,
e adiante, envolve a aplicação em um looping, onde serão capturadas as respostas do usuario e transformadas
em ação no motor (engine). A função main chama a handle_audio_input, onde irá trabalhar em threadings.
"""

def handle_audio_input():
    """
    Contém a lógica do sistema em looping
    """
    engine.engine_process_name(assistant.assist_name, assistant.person)

    while True:

        if not engine.actions:
            if not engine.greeting_exists:
                greeting = utils.get_greeting()
                voice_data = engine.engine_record_audio(f'{greeting}, {assistant.person}!')
            else:
                voice_data = engine.engine_record_audio(f'Bem vindo de volta, {assistant.person}!')
        else:
            voice_data = engine.engine_record_audio(f'Se quiser continuar, pode falar...')

        print('Por favor, aguarde... 🕓')
        engine.engine_response(voice_data)

        if not engine.control_system:
            break

def main():
    """
    Aplicação da lógica em threading
    """
    audio_thread = threading.Thread(target=handle_audio_input)
    audio_thread.start()

    # Loop principal do aplicativo
    while engine.control_system:
        pass  # Aqui você pode adicionar outras lógicas conforme necessário

if __name__ == "__main__":
    main()