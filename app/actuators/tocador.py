
def iniciar_tocador():
    print("iniciado")
    return None

def atuar_sobre_tocador(acao, objeto, _):
    if acao == "tocar" and objeto == "música":
        print("tocando a música")
    elif acao == "parar" and objeto == "música":
        print("parando a música")
