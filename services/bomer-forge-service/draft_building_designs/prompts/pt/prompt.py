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
