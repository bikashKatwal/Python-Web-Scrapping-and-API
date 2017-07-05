import requests
from datetime import date
from dateutil.rrule import rrule, DAILY

lat=input("Please enter latitude :")
lng=input("Please enter longitude :")
latlng=str(lat)+","+str(lng)

startdate=input("Please enter start date(YYYY/MM/DD) :")
enddate=input("Please enter end date(YYYY/MM/DD) :")
#print(latlng)

#current_data=requests.get('http://api.wunderground.com/api/ff3c6872140622ea/geolookup/conditions/forecast/q/-37.72000122,144.97000122.json').json()
current_data=requests.get('http://api.wunderground.com/api/ff3c6872140622ea/geolookup/conditions/forecast/q/'+latlng+'.json').json()
filename="WeatherData.csv"
f=open(filename,"w")
#headers="Date,Mean Temp(Actual), min Humidity,Max Humidity,Precipitation,Mean Pressure, Mean Wind Speed,Mean Wind Dir\n"
headers="Date,Temp,Humidity,Precipitation,Pressure,WindSpeed,WindDir\n"
f.write(headers)
def main():
    location =current_data['location']['city']
    temp_c=current_data['current_observation']['temp_c']
    wind_kph=str(current_data['current_observation']['wind_kph'])
    wind_dir=current_data['current_observation']['wind_dir']
    relative_humidity=current_data['current_observation']['relative_humidity']
    pressure_mb=current_data['current_observation']['pressure_mb']
    precip_today_metric=current_data['current_observation']['precip_today_metric']
    get_data(startdate,enddate)
    f.close()
    print("Current Temperature in %s is: %s \u00B0C" % (location, temp_c))
    print("Humidity : %s "% (relative_humidity))
    print("Wind : %s km/h %s"% (wind_kph,wind_dir))
    print("Pressure : %s hPa"%(pressure_mb))
    print("Precipitation : %s "%(precip_today_metric)+'%')
    

    
def get_precip(gooddate):    
    urlstart='http://api.wunderground.com/api/ff3c6872140622ea/history_'
    urlend = '/q/'+latlng+'.json'
    
    url=urlstart+str(gooddate)+urlend
    history_data=requests.get(url).json()
    #print(url)
    for summary in history_data['history']['dailysummary']:
        #date= str(summary['date']['year']+'-'+summary['date']['mon']+'-'+summary['date']['mday'])    
        date= str(summary['date']['year']+'-'+summary['date']['mon'])  
        mean_temp=summary['meantempm']
        #min_humidity=summary['minhumidity']
        max_humidity=summary['maxhumidity']
        precipitation=summary['precipm']
        mean_pressure=summary['meanpressurem']
        mean_windspeed=summary['meanwindspdm']
        mean_winddir=summary['meanwdire']
               
        #f.write(date+","+mean_temp+","+min_humidity+","+max_humidity+","+precipitation+","+mean_pressure+","+mean_windspeed+","+mean_winddir+ "\n")  
        f.write(date+","+mean_temp+","+max_humidity+","+precipitation+","+mean_pressure+","+mean_windspeed+","+mean_winddir+" \n")  
    
    
def get_data(startdate,enddate):
    startyear=int(startdate.split('/')[0])
    startmonth=int(startdate.split('/')[1])
    startday=int(startdate.split('/')[2])
    
    endyear=int(enddate.split('/')[0])
    endmonth=int(enddate.split('/')[1])
    endday=int(enddate.split('/')[2])    
   
    a=date(startyear,startmonth,startday)
    b = date(endyear, endmonth, endday)

    for dt in rrule(DAILY, dtstart=a, until=b):
        get_precip(dt.strftime("%Y%m%d"))
        
    
    print("Data imported to %s"%(filename))
    
  
main()
