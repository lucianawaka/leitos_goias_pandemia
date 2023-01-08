from TransformDados import TransformDados

class GenerateDados:
    
    def __init__(self):
        self.transform_dados = TransformDados()
        
    # Carrega os dados de leitos sus e não sus
    def create_df_leitos_sus_nsus_goias(self):
        self.transform_dados.transform_competen_to_datetime()
        self.transform_dados.create_year_column()
        self.transform_dados.create_df_leitos_sus_nsus_goias()
        self.transform_dados.to_csv_df_leitos_sus_nsus_goias()
        self.transform_dados.to_csv_df_lt()