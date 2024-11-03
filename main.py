import numpy as np
from extrator import Extrator
import rasterio
from rasterio.transform import from_origin

def calcular_volume(bacia_arr, dados_arr, dados_metadata):
    """
        Recebe dois np.array e um objeto contendo os dados.
        Calcula o volume em m³ e retorna um np.array contendo os
        volumes.
    """

    resolucao = dados_metadata.resolution
    # Converte a precipitação de mm para m
    converter_para_m = lambda valor: valor * 1e-3 
    # Calcula o volume de um pixel
    calcular_volume_pixel = lambda valor: converter_para_m(valor) * (resolucao ** 2)
    # Calcula o volume apenas nos pixels dentro da bacia
    volume_excedente = np.where(bacia_arr, calcular_volume_pixel(dados_arr), 0)
    return volume_excedente

def salvar_raster_tiff(volume, dados_metadata, transform, output_path, crs='EPSG:4326'):
    # Transforma o array unidimensional em duas dimensões para virar raster
    volume_2d = volume.reshape((dados_metadata.rows, dados_metadata.columns))

    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=volume_2d.shape[0],
        width=volume_2d.shape[1],
        count=1,  # Apenas uma banda/camada
        dtype=volume.dtype,
        crs=crs,
        transform=transform
    ) as raster:
        raster.write(volume_2d, 1)

def main():
    bacia_rdc_path = 'Watershed/watershed.RDC'
    bacia_rst_path = 'Watershed/watershed.RST'

    precip_rdc_path = 'Total excess precipitation/total_excess_precipitation.rdc'
    precip_rst_path = 'Total excess precipitation/total_excess_precipitation.rst'

    # Inicializa os extratores para os arquivos necessários
    bacia_rdc = Extrator(bacia_rdc_path)
    # precip_rdc = Extrator(precip_rdc_path) # Variável redundante pois os metadados utilizados são iguais 
    bacia_rst = Extrator(bacia_rst_path)
    precip_rst = Extrator(precip_rst_path)

    # Lê os dados de bacia e precipitação
    bacia_arr = np.genfromtxt(bacia_rst.arquivo)
    precip_arr = np.genfromtxt(precip_rst.arquivo)

    # Calcula o volume de escoamento
    volume = calcular_volume(bacia_arr, precip_arr, bacia_rdc)

    # Parâmetros usados para salvar o raster
    min_x = bacia_rdc.min_x
    max_y = bacia_rdc.max_y
    resolution = bacia_rdc.resolution

    # Cria a transformação para o raster
    transform = from_origin(min_x, max_y, resolution, resolution)

    # CRS padrão 'EPSG:4326'
    # O arquivo rdc possui uma linha ref. system: British National Grid
    # A partir dela é possível obter o crs correto que é 'EPSG:27700' 
    crs = 'EPSG:27700'

    # Salva o arquivo TIFF
    output_path = 'volume_escoamento.tif'
    salvar_raster_tiff(volume, bacia_rdc, transform, output_path, crs)

if __name__ == "__main__":
    main()
