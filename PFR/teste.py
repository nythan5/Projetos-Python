from datetime import datetime
from pytz import timezone

# Suponha que sua hora da coleta esteja na forma de string
hora_coleta_str = "01/08/2023 10:00:00"
data_hora_coleta = datetime.strptime(hora_coleta_str, "%d/%m/%Y %H:%M:%S")

# Crie um objeto de fuso horário para o Brasil (UTC-3:00)
fuso_horario_brasil = timezone("America/Sao_Paulo")

# Converta a hora da coleta para o fuso horário do Brasil
hora_coleta_final = data_hora_coleta.astimezone(fuso_horario_brasil)

# Formate a hora da coleta no formato desejado (12 horas)
hora_formatada = hora_coleta_final.strftime("%I:%M %p")

print(f"Hora da coleta: {hora_formatada}")
