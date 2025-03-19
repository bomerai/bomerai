import os
import ezdxf
from ezdxf.math import Vec2
from ai.services.runnables import get_gpt


def calculate_beam_length(dxf_file_path, layer_name="linhas"):
    try:
        # Carregar o arquivo DXF
        doc = ezdxf.readfile(dxf_file_path)
        msp = doc.modelspace()  # Model Space contém as entidades

        total_length = 0.0

        # Filtrar entidades LINE no layer especificado
        for entity in msp.query('LINE[layer=="{}"]'.format(layer_name)):
            start = Vec2(entity.dxf.start)  # Ponto inicial (x, y)
            end = Vec2(entity.dxf.end)  # Ponto final (x, y)
            length = start.distance(end)  # Comprimento da linha
            total_length += length

        return total_length

    except Exception as e:
        print(f"Erro ao processar o arquivo DXF: {e}")
        return None


def get_pormenores(dxf_file_path, layer_name=".pormenores"):
    try:
        doc = ezdxf.readfile(dxf_file_path)
        msp = doc.modelspace()

        pormenores = []
    except Exception as e:
        print(f"Erro ao processar o arquivo DXF: {e}")
        return None


# Exemplo de uso
dxf_path = os.path.join(os.path.dirname(__file__), "input.dxf")
layer = "linhas"
length = calculate_beam_length(dxf_path, layer)

if length is not None:
    print(f"Comprimento total das vigas no layer '{layer}': {length:.2f} unidades")
