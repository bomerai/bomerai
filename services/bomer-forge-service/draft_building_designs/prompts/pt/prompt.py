from pydantic import BaseModel, Field
from typing import Literal


class Sapata(BaseModel):
    largura: float = Field(..., description="A largura da sapata em centimetros")
    comprimento: float | None = Field(
        None,
        description="O comprimento da sapata em centimetros caso exista. Caso não exista, considere que a sapata é um muro de fundação (ou viga de fundação) e adicione 0 ao comprimento da sapata.",
    )
    altura: float = Field(..., description="A altura da sapata em centimetros")
    armadura_inferior_x: str | None = Field(
        None, description="Valores de armadura inferior da sapata. Exemplo: 13Ø12a/13"
    )
    armadura_inferior_y: str | None = Field(
        None, description="Valores de armadura inferior da sapata. Exemplo: 13Ø12a/13"
    )
    armadura_superior_x: str | None = Field(
        None, description="Valores de armadura superior da sapata. Exemplo: 13Ø12a/13"
    )
    armadura_superior_y: str | None = Field(
        None, description="Valores de armadura superior da sapata. Exemplo: 13Ø12a/13"
    )
    referencias: str | None = Field(
        None,
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


def get_extract_footings_from_design_drawing_document_prompt() -> tuple[str, str]:
    """Returns the prompt for extracting footing metadata in Portuguese"""
    return (
        prompt_text_v2,
        Sapatas.__name__,
    )


# -


class PilarBase(BaseModel):
    codigo: str | None = Field(None, description="O codigo do pilar. Exemplo: P1=P2=P3")


class Pilar(PilarBase):
    largura: float = Field(..., description="A largura do pilar em centimetros")
    comprimento: float = Field(..., description="O comprimento do pilar em centimetros")
    altura: float = Field(
        ...,
        description="A altura do pilar em centimetros caso exista, é a soma dos intervalos da distribuicao dos estribos no arranque e na armadura longitudinal",
    )
    armadura_longitudinal: str = Field(
        ...,
        description="O diametro e quantidade da armadura longitudinal do pilar. Exemplo: 4Ø12",
    )
    estribos: str = Field(
        ...,
        description="O diametro e quantidade de estribos do pilar, também conhecido como armadura transversais. Exemplo: 24Ø8",
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
        - A tabela possui células e o cabeçalho da tabela possui os identificadores dos pilares.
        - As células são as informações de cada grupo de pilar. Exemplo: P1=P2=P3, P4=P5, P6=P7=P8=P9=P10. Abaixo do cabeçalho pode haver uma ou duas caixas indicando que há configurações diferentes para a coluna dependendo do piso.
        - Uma célula pode estar divida em duas caixas, cada qual contendo informações de intervalos e estribos diferentes, indicando que há configurações diferentes para a coluna dependendo do piso. Nesse caso, extraia cada caixa separadamente mantendo o mesmo código do grupo de pilares.
        - Algumas células podem conter mais de um pilar, sendo identificados por múltiplas letras ou números, por exemplo: P1=P2=P3 significa que a célula contém os pilares P1, P2 e P3.
        - Todos os identificadores de pilares devem ser extraídos corretamente e preservados.
        - **Analise cada célula separadamente e extraia os dados de cada pilar.**

        **Registro das Armaduras:**
        - A armadura longitudinal sempre deve ser extraída e registrada corretamente.
        - As armaduras transversais (estribos) devem ser extraídas conforme as tabelas e preservadas separadamente se houver mais de uma.
        - Caso existam diferentes tipos de distribuição de estribos dentro do mesmo pilar, **todas as distribuições devem ser mantidas no JSON**.

        **Como calcular a altura do pilar:**
        - A altura do pilar é **a soma da diferença entre o maior e o menor valor de todos os intervalos indicados na tabela. Exemplo: se os intervalos são [100-400, 0-100], a altura do pilar é 400cm - 0cm = 400cm, se os intervalos são [0-300], a altura do pilar é 300cm - 0cm = 300cm**.
        - A altura do arranque **não deve ser incluída** no cálculo da altura do pilar principal.

        **Como identificar os pilares IPE:**
        - Se um pilar for do tipo IPE, ele será representado por um retângulo com a descrição "IPE". Exemplo: IPE 200.
        - Para cada pilar IPE encontrado, registre um novo objeto `PilarIPE` com a descrição correta.

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

columns_prompt_text_v3 = """
        Você é um assistente técnico especializado em engenharia estrutural. Sua tarefa é analisar imagens de detalhamento de pilares (como plantas de formas ou armação) e extrair informações estruturadas em formato JSON para posterior uso em um sistema de cálculo automático de estruturas.

        **Sua resposta deve ser um JSON válido seguindo o seguinte schema:**
        {schema}

        Regras e Observações:
        - A altura deve ser calculada com base na soma dos intervalos de estribos descritos no detalhamento (como “0 a 335 cm” ou “0 a 100 cm”).
        - Caso haja trechos adicionais como “arranque”, ignore-os.
        - O campo armadura_longitudinal representa a quantidade e diâmetro das barras longitudinais do pilar.
        - O campo estribos representa a armadura transversal (também chamada de estribo), incluindo diâmetro e quantidade de estribos.
        - A quantidade de estribos é a soma dos números de estribos presente ta tabela de intervalos.
        - Se houver múltiplos blocos de informação (por exemplo, diferentes intervalos ou trechos), consolide os dados em um único objeto.
        """


def get_extract_column_from_design_drawing_file_prompt() -> tuple[str, str]:
    """Returns the prompt for extracting column metadata in Portuguese"""
    return (
        columns_prompt_text_v3,
        Pilar.__name__,
    )


# -


class Calculo(BaseModel):
    volume_de_betao_em_metros_cubicos: float = Field(
        ..., description="O volume de betão em metros cúbicos"
    )
    peso_da_armadura_em_quilogramas: float = Field(
        ..., description="O peso da armadura quilogramas"
    )
    raciocinio: str = Field(
        ...,
        description="O raciocinio para chegar ao calculo de quantidade de materiais",
    )


def get_generate_component_bom_prompt() -> tuple[str, str]:
    """Returns the prompt for calculating the BOM for a footing in Portuguese"""
    return (
        """
        Você é um especialista em engenharia civil. Seu objetivo é calcular o volume de betão e o peso da armadura de um componente de fundação. Calcule o volume de betão e o peso da armadura para o componente especificado e retorne o componente com o volume de concreto e o peso da armadura. Os componentes de fundação podem ser: sapata, viga de equilíbrio ou pilare IPE.

        **Caso o componente não especifique uma das armaduras, faça o cálculo com as armaduras existentes e ignore a armadura que não está especificada. O importante é sempre calcular o volume de betão e o peso da armadura.**
        
        *O contexto contem as medidas de um componente de um projeto de estrutura no formato JSON para calcular o volume de betão e o peso da armadura*

        {context}

        **Saida de dados:**
        - volume_de_betao_em_metros_cubicos: O volume de betão em metros cúbicos, caso não seja possível calcular, retorne 0
        - peso_da_armadura_em_quilogramas: O peso da armadura em quilogramas, caso não seja possível calcular, retorne 0
        - raciocinio: O raciocinio para chegar ao calculo de quantidade de materiais

        *Dicionario de dados:*
        13Ø12a/13 -> 13Ø12 a 13cm
        Ø8/30 -> 30 unidades de Ø8 espaçadas de acordo com a largura/comprimento do componente se especificado.
        """,
        Calculo.__name__,
    )


# -


class Bom(BaseModel):
    pass


building_design_building_components_extraction_prompt_text = """
        Você é um especialista em engenharia civil. Você consegue interpretar plantas estruturais e extrair informações precisas sobre os pilares representados. Seu objetivo é criar um modelo de componente para cada componente que está representado na imagem e retorná-los no formato JSON.

        **Como gerar os componentes:**
        - Uma imagem de uma planta estrutural contém várias colunas e sapatas. 
        - Todas as colunas e sapatas que estão representadas na imagem existem no contexto abaixo.
        - Leia a imagem e use o contexto abaixo para identificar quais componentes estão representados na imagem.
        - IMPORTANTE: Identifique primeiro os pilares e depois as sapatas.
        - Após identificar os metadados dos componentes, retorne uma lista com todos os componentes criados para cada tipo que for identificado na imagem a partir do contexto.

        **Escolhendo os pilares:**
        - As sapatas geralmente possuem uma referência de código que identifica os pilares que estão apoiados nelas. Use essa informação para identificar os pilares.
        - Metadados de pilares possuem um código com um ou mais identificadores de pilares. Na imagem, haverá uma referência de código para cada pilar. Retorne apenas o código do pilar, não retorne o código da sapata ou referência de código de pilares.

        **Escolhendo as sapatas:**
        - Cada pilar individual deve ter uma sapata correspondente, a menos que a sapata seja do tipo corrida, onde um único elemento pode suportar múltiplos pilares.
        - Se houver 4 pilares (P1, P2, P3, P4) e as sapatas forem do tipo isolada, o resultado final deve conter 4 sapatas diferentes, cada uma associada a um pilar diferente.
        - Se houver 4 pilares e a sapata for do tipo corrida, então apenas uma sapata deve ser criada, e todos os 4 pilares devem ser referenciados como apoiados nela.
        - As sapatas podem ter diferentes formatos: retangulares, circulares ou irregulares.
        - As sapatas podem ter uma ou mais vigas de equilíbrio.
        - As sapatas podem ter um ou mais pilares IPE apoiados nelas.
        - Use o código do pilar especificado na imagem e a forma geométrica da sapata para identificar qual sapata corresponde ao pilar.

        **Exemplos:**
        - Se na imagem aparecerem 8 pilares com sapatas isoladas, o JSON deve conter **8 sapatas, cada uma associada a um pilar diferente**.
        - Se na imagem aparecerem 8 pilares apoiados em uma sapata corrida, o JSON deve conter **apenas 1 sapata corrida**, referenciando os 8 pilares apoiados nela.

        {context}
        """


def get_building_design_building_components_extraction_prompt() -> tuple[str, str]:
    """Returns the prompt for extracting building design components in Portuguese"""
    return (
        building_design_building_components_extraction_prompt_text,
        Bom.__name__,
    )


# -


class Viga(BaseModel):
    pass
