class ArquivoTxt(object): 
    #Inicializando a classe com seus atriputos 
    def __init__(self, nome_arquivo: str): 
        self.nome_arquivo = nome_arquivo
        self.conteudo = self._leitura_conteudo()
    

    def _leitura_conteudo(self): 
        #função para fazer a leitura do arquivo
        conteudos = []
        with open(file = self.nome_arquivo, mode = 'r', encoding='utf8') as fp: 
            linha = fp.readline() #comando para ler apenas uma linha
            while linha: 
                conteudo = linha.strip().split(',') #tira os espaços e quebra em virgula
                conteudos.append(conteudo)
                linha = fp.readline()
        return conteudos
    

    def extrair_colunas(self, indice_coluna: int): 
        #Extraio apenas a coluna desejada
        coluna = []
        for linha in self.conteudo: 
            conteudo_linha = linha
            coluna.append(conteudo_linha[indice_coluna])
        return coluna


    def __str__(self):
        #apenas para retornar o conteudo caso eu chamo o comando (dados_irradiacao_318.conteudo) retorna o conteudo lido. 
        return str(self.conteudo)