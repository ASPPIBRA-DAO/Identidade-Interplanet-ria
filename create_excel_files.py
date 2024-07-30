from openpyxl import Workbook

# Criar Record.xlsx
record_wb = Workbook()  # Cria um novo arquivo Excel
record_ws = record_wb.active  # Seleciona a planilha ativa
record_ws.append(["Name", "Branch", "Year"])  # Adiciona cabeçalho das colunas
record_ws.append(["aluno_01", "CSE", 1])  # Adiciona dados de exemplo
record_ws.append(["aluno_02", "ECE", 2])
record_wb.save("Record.xlsx")  # Salva o arquivo Excel com o nome "Record.xlsx"

# Criar attendence.xlsx
attendence_wb = Workbook()  # Cria um novo arquivo Excel
attendence_ws = attendence_wb.active  # Seleciona a planilha ativa
attendence_ws.append(["Name", "Year", "Branch", "Time In", "Time Out"])  # Adiciona cabeçalho das colunas
attendence_wb.save("attendence.xlsx")  # Salva o arquivo Excel com o nome "attendence.xlsx"

print("Arquivos Record.xlsx e attendence.xlsx criados com sucesso.")
