from db_models import get_session, Moodel 
import os


def TOmarkdown(city_name):
    s=get_session()#создаем сессию...не зимняя:)
    zaprosi=s.query(Moodel).filter_by(city=city_name).order_by(Moodel.forecast_date).all()
    
    if not zaprosi: 
        print("Нету ничего")
        return

    output_file=os.getenv("OUTPUT_FILE", "weather_report.md") 
    date0=zaprosi[0].forecast_date
    date1=zaprosi[-1].forecast_date
    
    lines=[]
    lines.append("# Прогноз погоды")
    lines.append(f"Lокация: {city_name}")
    lines.append(f"Даты: {date0} – {date1}")
    lines.append("")
    lines.append("| Дата    :)   | Мини. темп. :() | Макси. темп. ;(| Описание    :D        | Влажность ;P | Ветер :.>|")
    lines.append("|--------------|-----------------|----------------|-----------------------|--------------|----------|")
    
    for x in zaprosi:
        lines.append(f"| {x.forecast_date} | {x.temp_min:<15} | {x.temp_max:<16} | {x.description:<21} | {x.humidity:<13} | {x.wind_speed:<11} |")   
    content="\n".join(lines)
    
    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write(content)
        
    print(f"[Export] Сохрагили {output_file}")
    s.close()