from pydantic import BaseModel, Field


class Sapata(BaseModel):
    largura: float | None = Field(
        None, description="A largura da sapata em centimetros"
    )
    comprimento: float | None = Field(
        None, description="O comprimento da sapata em centimetros"
    )
    altura: float | None = Field(None, description="A altura da sapata em centimetros")
    armadura_inferior_x: str | None = Field(
        None, description="A armadura inferior da sapata em centimetros"
    )
    armadura_inferior_y: str | None = Field(
        None, description="A armadura inferior da sapata em centimetros"
    )
    armadura_superior_x: str | None = Field(
        None, description="A armadura superior da sapata em centimetros"
    )
    armadura_superior_y: str | None = Field(
        None, description="A armadura superior da sapata em centimetros"
    )
    justificacao: str | None = Field(
        None, description="A justificacao para a escolha dos dados da sapata"
    )


def get_extract_footing_metadata_from_design_drawing_document_prompt() -> (
    tuple[str, str]
):
    """Returns the prompt for extracting footing metadata in Portuguese"""
    return (
        """Você é um especialista em engenharia civil. Seu objetivo é extrair metadados de uma imagem de uma sapata. A imagem está em português e ela é um corte transversal de uma sapata com uma vista lateral. Se alguns dos dados não estão visíveis na imagem, use o conhecimento do engenheiro civil para estimar o valor. Use o seguinte JSON schema: {schema}""",
        Sapata.__name__,
    )


# -


class Pilar(BaseModel):
    codigo: str | None = Field(None, description="O codigo do pilar. Exemplo: P1=P2=P3")
    largura: float | None = Field(None, description="A largura do pilar em centimetros")
    comprimento: float | None = Field(
        None, description="O comprimento do pilar em centimetros"
    )
    altura: float | None = Field(None, description="A altura do pilar em centimetros")
    armadura_longitudinal_diametro: str | None = Field(
        None, description="O diametro da armadura longitudinal do pilar"
    )
    armadura_longitudinal_estribos_numero: int | None = Field(
        None, description="O numero de estribos da armadura longitudinal do pilar"
    )
    armadura_longitudinal_estribos_espacamento: float | None = Field(
        None, description="O espacamento dos estribos da armadura longitudinal do pilar"
    )
    armadura_longitudinal_intervalos: list[str] | None = Field(
        None,
        description="Os intervalos da armadura longitudinal do pilar. Exemplo: ['100-400', '0-100']",
    )
    arranque_diametro: str | None = Field(
        None,
        description="O diametro do arranque da armadura longitudinal do pilar. Geralmente o mesmo valor que a armadura longitudinal.",
    )
    arranque_estribos_numero: int | None = Field(
        None,
        description="O numero de estribos do arranque da armadura longitudinal do pilar",
    )
    arranque_estribos_espacamento: float | None = Field(
        None,
        description="O espacamento dos estribos do arranque da armadura longitudinal do pilar",
    )
    estribo_diametro: str | None = Field(
        None, description="O diametro do estribo do pilar"
    )
    nivel: int | None = Field(
        None,
        description="O nível do pilar. Para solo o valor é 0, primeiro andar 1 e assim por diante.",
    )
    justificacao: str | None = Field(
        None, description="A justificacao para a escolha dos dados do pilar"
    )


class Pilares(BaseModel):
    pilares: list[Pilar]


def get_extract_columns_metadata_from_design_drawing_file_prompt() -> tuple[str, str]:
    """Returns the prompt for extracting column metadata in Portuguese"""
    return (
        """
        Você é um especialista em engenharia civil. Seu objetivo é extrair metadados de uma imagem que contem vários pilares. 
        
        *Ao calcular a altura da coluna, considere que a altura é dada pela soma dos intervalos da armadura e não inclui o arranque.*
        
        *Cada pilar esta dentro de um retangulo e alguns retangulos podem conter mais de um pilar.*

        *O diametro da armadura longitudinal e o diametro do arranque são iguais e deve vir junto com a quantidade, exemplo: 4Ø12.*
        
        Considere que um retangulo pode conter um pilar ou vários. Se alguns dos dados não estão visíveis na imagem, use o conhecimento do engenheiro civil para estimar o valor. Use o seguinte JSON schema: {schema}""",
        Pilares.__name__,
    )
