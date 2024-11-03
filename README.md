# Mapa de Volume de Chuva Excedente

Este projeto tem como objetivo gerar um mapa de volume de chuva excedente por unidade hidrológica (pixels da bacia fornecida) a partir do arquivo de chuva excedente. O código utiliza as bibliotecas NumPy e Rasterio para processar dados matriciais e gerar um arquivo raster no formato TIFF.

## Dependências

*   numpy
*   rasterio

Você pode instalar as dependências necessárias usando o seguinte comando:

```
pip install -r requirements.txt
```
## Como Usar

1. **Configuração dos Arquivos**: Os arquivos `.RDC` e `.RST` devem estar nas pastas correspondentes (`Watershed` e `Total excess precipitation`).
2. **Executar o Script**: Execute o script principal:

    python main.py
    
3.  **Resultado**: O resultado será um arquivo `volume_escoamento.tif` gerado na pasta do projeto, contendo o volume de chuva excedente.

## Detalhes do Código

### Classe `Extrator`

A classe `Extrator` é responsável por ler os arquivos RST e RDC e extrair informações como:

*   Número de linhas e colunas
*   Resolução
*   Coordenadas mínimas e máximas

Além de poder mostrar todo o conteúdo do arquivo.

### Função `calcular_volume`

Esta função calcula o volume de escoamento usando os dados de precipitação e a máscara da bacia hidrográfica.

### Função `salvar_raster_tiff`

Esta função salva o volume calculado em um arquivo raster no formato TIFF.