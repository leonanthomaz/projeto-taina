
import time
import re

"""
Arquivo utilitário. Possui função de horario para saudação, checagem de termos válidos para
as pesquisas de resposta do motor e extração de url para pegar determinado site.
"""

def get_greeting():
    """
    Saudação baseada no horário
    """
    current_hour = int(time.strftime('%H'))

    if 6 <= current_hour < 12:
        return 'Bom dia'
    elif 12 <= current_hour < 18:
        return 'Boa tarde'
    else:
        return 'Boa noite'

def engine_check(terms, voice_data):
    """
    Função pra identificar se o termo existe
    """
    for term in terms:
        if term in voice_data:
            return True
    return False

def extract_domain(url):
    """
    Extrai o domínio de uma URL.

    Args:
        url (str): A URL da qual extrair o domínio.

    Returns:
        str: O domínio extraído, ou uma string vazia se não for possível extrair.
    """
    pattern = r"www\.(.*?)\.com"
    matches = re.findall(pattern, url)
    if matches:
        return matches[0]
    else:
        return url