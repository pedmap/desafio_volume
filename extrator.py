import re

class Extrator:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.rows = None
        self.columns = None
        self.resolution = None
        self.min_x = None
        self.min_y = None
        self.max_x = None
        self.max_y = None
        self.data = None
        self._ler_arquivo()

    def _ler_arquivo(self):
        """Lê o arquivo e extrai as informações necessárias."""
        with open(self.arquivo, encoding="latin-1") as f:
            self.data = f.read()
        
        # Regex para capturar informações
        self.rows = self._extrair_info(r"rows\s*:\s*(\d+)")
        self.columns = self._extrair_info(r"columns\s*:\s*(\d+)")
        self.resolution = self._extrair_info(r"resolution\s*:\s*(\d+\.\d+)", float)
        self.min_x = self._extrair_info(r"min\.\s*X\s*:\s*(\d+\.\d+)", float)
        self.min_y = self._extrair_info(r"min\.\s*Y\s*:\s*(\d+\.\d+)", float)
        self.max_x = self._extrair_info(r"max\.\s*X\s*:\s*(\d+\.\d+)", float)
        self.max_y = self._extrair_info(r"max\.\s*Y\s*:\s*(\d+\.\d+)", float)

    def _extrair_info(self, padrao, tipo=int):
        """
            Extrai informações do texto baseado em uma regex.
            As informações estão no grupo 1 (após o ":")
        """
        match = re.search(padrao, self.data, flags=re.IGNORECASE)
        return tipo(match.group(1)) if match else None
