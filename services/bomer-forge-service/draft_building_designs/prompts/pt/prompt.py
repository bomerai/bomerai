from pydantic import BaseModel, Field
from typing import Literal


class Sapata(BaseModel):
    largura: float = Field(..., description="A largura da sapata em centimetros")
    comprimento: float | None = Field(
        None,
        description="O comprimento da sapata em centimetros caso exista. Caso não exista, considere que a sapata é um muro de fundação (ou viga de fundação) e adicione 0 ao comprimento da sapata.",
    )
    altura: float = Field(..., description="A altura da sapata em centimetros")
    armadura_inferior_x: str = Field(
        ..., description="A armadura inferior da sapata em centimetros"
    )
    armadura_inferior_y: str = Field(
        ..., description="A armadura inferior da sapata em centimetros"
    )
    armadura_superior_x: str = Field(
        ..., description="A armadura superior da sapata em centimetros"
    )
    armadura_superior_y: str = Field(
        ..., description="A armadura superior da sapata em centimetros"
    )
    referencias: str = Field(
        ...,
        description="Os codigos dos pilares que estao apoiados na sapata caso existam. Exemplo: P1=P2=P3",
    )
    tipo: Literal["Sapata Isolada", "Sapata Corrida"] = Field(
        ..., description="O tipo de sapata"
    )
    justificacao: str = Field(
        ..., description="A justificacao para a escolha dos dados da sapata"
    )


class Sapatas(BaseModel):
    sapatas: list[Sapata]


prompt_text_v1 = """Você é um especialista em engenharia civil. Seu objetivo é extrair metadados de uma imagem de uma sapata. A imagem está em português. Ela pode mostrar uma ou mais saptatas. Ela pode conter um ou mais pilares apoiados na sapata. Se alguns dos dados não estão visíveis na imagem, use o conhecimento do engenheiro civil para estimar o valor. Use o seguinte JSON schema: {schema}"""

prompt_text_v2 = """Você é um especialista em engenharia civil. Você é um ótimo engenheiro pois você consegue ler uma planta de estrutura e entender o que está sendo representado. Seu objetivo é extrair metadados de uma sapata em uma imagem de um projeto de estrutura. A imagem está em português. Ela pode mostrar uma ou mais saptatas.

Ao extrair os dados da sapata, considere que:
- A sapata é um elemento de fundação que transfere as cargas dos pilares para o solo.
- Os metadados da sapata são os dados que descrevem a geometria e a armadura da sapata.
- Algumas imagens mostrar um corte transversal da sapata e outras mostrarão uma tabela com os dados da sapata.
    - Caso a imagem seja um corte transversal, a sapata é do tipo "Sapata Corrida" e possui um muro de fundação ou viga de fundação. Nesse caso ela não possui comprimento, mas obrigatoriamente possui largura e altura.
    - Caso a imagem seja uma tabela, a sapata é do tipo "Sapata Isolada" e possui largura, comprimento e altura.
- A armadura inferior da sapata é a armadura que está na parte inferior da sapata.
- A armadura superior da sapata é a armadura que está na parte superior da sapata.


Use o seguinte JSON schema para extrair os dados da sapata: {schema}"""


def get_extract_footing_metadata_from_design_drawing_document_prompt() -> (
    tuple[str, str]
):
    """Returns the prompt for extracting footing metadata in Portuguese"""
    return (
        prompt_text_v2,
        Sapatas.__name__,
    )


# -

Pisos = Literal["o", "1o", "2o", "3o", "4o", "5o", "6o", "7o", "8o", "9o", "10o"]


class PilarBase(BaseModel):
    codigo: str | None = Field(None, description="O codigo do pilar. Exemplo: P1=P2=P3")
    pisos: list[Pisos] = Field(
        ..., description="Os pisos que o pilar atinge. Exemplo: [1o, 2o]"
    )
    tipo: Literal["0", "1"] = Field(..., description="O tipo de pilar")


class DistribuicaoPilarEstribos(BaseModel):
    intervalo: str = Field(..., description="O intervalo do pilar. Exemplo: '100-400'")
    numero: int = Field(..., description="Número de estribos")
    espacamento: float = Field(
        ..., description="O espaçamento dos estribos em centimentros"
    )


class DistribuicaoPilarArranqueEstribos(BaseModel):
    numero: int = Field(..., description="Número de estribos")


class Pilar(PilarBase):
    largura: float = Field(..., description="A largura do pilar em centimetros")
    comprimento: float = Field(..., description="O comprimento do pilar em centimetros")
    altura: float = Field(
        ...,
        description="A altura do pilar em centimetros caso exista, se não existir, considere 0",
    )
    armadura_longitudinal: str = Field(
        ...,
        description="O numero e o diametro da armadura longitudinal do pilar. Exemplo: 4Ø12",
    )
    pilar_estribos: list[DistribuicaoPilarEstribos] = Field(
        ...,
        description="A distribuicao dos estribos da armadura longitudinal do pilar",
    )
    arranque: str = Field(
        ...,
        description="O diametro do arranque da armadura longitudinal do pilar. Geralmente o mesmo valor que a armadura longitudinal. Exemplo: 4Ø12",
    )
    arranque_estribos: list[DistribuicaoPilarArranqueEstribos] = Field(
        ...,
        description="A distribuicao dos estribos do arranque da armadura longitudinal do pilar",
    )
    estribo_diametro: str = Field(
        ...,
        description="O diametro do estribo do pilar",
    )


class PilarIPE(PilarBase):
    descricao: str = Field(..., description="A descrição do pilar. Exemplo: IPE 200")
    altura: float | None = Field(
        None,
        description="A altura do pilar em centimetros caso exista, se não existir, considere 0",
    )


class Pilares(BaseModel):
    pilares: list[Pilar | PilarIPE]


columns_prompt_text_v1 = """
        Você é um especialista em engenharia civil. Você é um ótimo engenheiro pois você consegue ler uma planta de estrutura e entender o que está sendo representado. Seu objetivo é extrair metadados de uma imagem que contem vários pilares.

        **Como identificar os pilares:**
        - Alguns retangulos podem conter mais de um pilar. Sendo identifications com letras, exemplo: P1=P2=P3 que significa que o retangulo contem os pilares P1, P2 e P3.
        - Alguns retangulos podem conter apenas um pilar. Sendo identifications com letras, exemplo: P1 que significa que o retangulo contem o pilar P1.
        - Os pilares obrigatoriamente possuem uma largura e um comprimento.

        **Como identificar os pilares IPE:**
        - Alguns retangulos podem conter um pilar IPE.
        - Os pilares IPE são representados por retangulos com a descrição "IPE". Exemplo: IPE 200.
        - Você deve retornar um novo objeto PilarIPE para cada retangulo com a descrição "IPE", sendo a descrição o valor da descrição do retangulo. Exemplo: PilarIPE(descricao="IPE 200", altura=0).
        
        **Como calcular a altura do pilar:**
        - A Altura do pilar é dada pela soma dos intervalos. Exemplo: se os intervalos são [100-400, 0-100], a altura do pilar é 400cm.
        - A altura do pilar não leva em consideração a altura do arranque.

        **Como calcular a altura do arranque:**
        - A altura do arranque é dada pela soma da altura da sapata com o comprimento da ancoragem.
        - A altura da sapata está especificada no contexto de acordo com o código do pilar.
        - O comprimento da ancoragem é dado pela multiplicação do diâmetro da armadura pelo fator 40. Exemplo: Se o diâmetro da armadura é 12mm, o comprimento da ancoragem é 40 \times 12 = 480mm, logo a altura do arranque caso a sapata seja de 60cm é 60cm + 48cm = 108cm.

        Segue a altura das sapatas e os pilares apoiados nelas:
        {context}

        **OBS: Para definir o pisos, considere que o pisos é onde o pilar começa e termina. Exemplo: se o pilar começa na fundação e termina no Piso 1, o piso é o. Se o pilar começa na fundação e termina no Piso 2, o piso é o e o1. Se o pilar começa na fundação e termina no Piso 3, o piso é o e o1 e o2.**

        Se alguns dos dados não estão visíveis na imagem, use o conhecimento do engenheiro civil para estimar o valor. Use o seguinte JSON schema: {schema}"""

columns_prompt_text_v2 = """
        Você é um especialista em engenharia civil. Você consegue interpretar plantas estruturais e extrair informações precisas sobre os pilares representados. Seu objetivo é extrair metadados de uma imagem que contém vários pilares.

        **Identificação dos Pilares:**
        - Alguns retângulos podem conter mais de um pilar, sendo identificados por múltiplas letras ou números, por exemplo: P1=P2=P3 significa que o retângulo contém os pilares P1, P2 e P3.
        - Todos os identificadores de pilares devem ser extraídos corretamente e preservados.

        **Extração de Dados das Tabelas:**
        - Cada pilar pode conter **uma ou mais tabelas de distribuição de estribos**.
        - **Extraia cada tabela separadamente antes de qualquer unificação de informações.**
        - Se houver duas tabelas para o mesmo pilar, ambas devem ser **preservadas** no JSON de saída antes de qualquer fusão de dados.
        - **Exemplo de extração correta**:
            - Tabela 1: Intervalo: 0-335, Número: 22, Espaçamento: 15
            - Tabela 2: Intervalo: 0-100, Número: 7, Espaçamento: 15
            - **Saída JSON correta:**  
              ```json
              "distribuicao_estribos": [
                {{"intervalo": "0-335", "numero": 22, "espacamento": 15}},
                {{"intervalo": "0-100", "numero": 7, "espacamento": 15}}
              ]
              ```
              ```
        - Se houver um **arranque separado na tabela**, ele deve ser registrado explicitamente e NÃO mesclado com os intervalos principais.

        **Registro das Armaduras:**
        - A armadura longitudinal sempre deve ser extraída e registrada corretamente.
        - As armaduras transversais (estribos) devem ser extraídas conforme as tabelas e preservadas separadamente se houver mais de uma.
        - Caso existam diferentes tipos de distribuição de estribos dentro do mesmo pilar, **todas as distribuições devem ser mantidas no JSON**.

        **Como calcular a altura do pilar:**
        - A altura do pilar é **a soma de todos os intervalos indicados na tabela**.
        - A altura do arranque **não deve ser incluída** no cálculo da altura do pilar principal.
        - Se houver mais de uma tabela para um mesmo pilar, **soma-se todos os intervalos antes de definir a altura final**.

        **Como identificar os pilares IPE:**
        - Se um pilar for do tipo IPE, ele será representado por um retângulo com a descrição "IPE". Exemplo: IPE 200.
        - Para cada pilar IPE encontrado, registre um novo objeto `PilarIPE` com a descrição correta.

        **Pisos do Pilar:**
        - O piso do pilar deve ser registrado corretamente conforme sua altura.
        - Exemplo: se o pilar começa na fundação e termina no Piso 1, o piso é `["P0"]`. Se começa na fundação e termina no Piso 2, o piso é `["P0", "P1"]`.

        **Vocabulário:**
        - Ø: Diâmetro
        - Arm. Long.: Armadura Longitudinal
        - Armaduras transversais: Estribos
        - Intervalo: Faixa de aplicação dos estribos
        - Número: Quantidade de estribos dentro do intervalo
        - Separação: Distância entre estribos dentro do intervalo
        - Arranque: Parte inicial da armadura que não deve ser misturada com os intervalos principais.

        **IMPORTANTE:**  
        Se algum dado não estiver visível na imagem, utilize **conhecimento de engenharia civil** para estimar valores plausíveis. O retorno deve seguir o seguinte JSON schema: {schema}
        """


def get_extract_columns_metadata_from_design_drawing_file_prompt() -> tuple[str, str]:
    """Returns the prompt for extracting column metadata in Portuguese"""
    return (
        columns_prompt_text_v2,
        Pilares.__name__,
    )


# -


class Sapatacdq(BaseModel):
    uuid: str
    volume_de_betao_em_metros_cubicos: float = Field(
        ..., description="O volume de betão em metros cúbicos"
    )
    peso_da_armadura_em_quilogramas: float = Field(
        ..., description="O peso da armadura quilogramas"
    )
    justificacao: str = Field(
        ..., description="A justificacao do calculo de quantidade de materiais"
    )
    raciocinio: str = Field(
        ...,
        description="O raciocinio para chegar ao calculo de quantidade de materiais",
    )


class Sapatacdqs(BaseModel):
    sapatacdqs: list[Sapatacdq]


def get_calculate_bom_for_footing_prompt() -> tuple[str, str]:
    """Returns the prompt for calculating the BOM for a footing in Portuguese"""
    return (
        """
        Você é um especialista em engenharia civil. Seu objetivo é calcular o volume de betão e o peso da armadura de uma sapata. Calcule o volume de betão e o peso da armadura para cada sapata e retorne a sapata com o volume de concreto e o peso da armadura e o uuid da sapata.
        
        *O contexto contem uma sapata no formato JSON*

        {context}

        *Dicionario de dados:*
        13Ø12a/13 -> 13Ø12 a 13cm
        Ø8/30 -> 30 unidades de Ø8 espaçadas de acordo com a largura/comprimento da sapata
        """,
        Sapatacdq.__name__,
    )
