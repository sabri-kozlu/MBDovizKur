import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from datetime import datetime, timedelta
import pyodbc
import time
start_date = datetime(2013, 1, 1)
end_date = datetime(2023, 7, 28)
# Veritabanı bağlantısı ve tablo oluşturma
date = start_date
usd_buy_rate=0;
usd_sell_rate=0;
eur_buy_rate=0;
eur_sell_rate=0;
query = """INSERT INTO GunlukKurDegerleri (usd_alis,usd_satis,eur_alis,eur_satis,tarih) VALUES (?,?,?,?,?)"""

conn2 = pyodbc.connect('')
cursor1 = conn2.cursor()
while date <= end_date:
        yil=date.strftime(format='%Y');
        ay=date.strftime(format='%m');
        gun=date.strftime(format='%d');
        api_url="https://www.tcmb.gov.tr/kurlar/"+str(yil)+str(ay)+"/"+str(gun)+str(ay)+str(yil)+".xml";
        print(date);
        print(api_url);

        try:
           response = requests.get(api_url)
           time.sleep(3)
           if response.status_code == 200:
               # XML yanıtını işleyin
               root = ET.fromstring(response.content)
               
               # USD ve EURO alış ve satış kurlarını çıkartın
               for currency in root.findall('.//Currency'):
                   if currency.get('Kod') == 'USD':
                       usd_buy_rate = float(currency.find('ForexBuying').text)
                       usd_sell_rate = float(currency.find('ForexSelling').text)
                   elif currency.get('Kod') == 'EUR':
                       eur_buy_rate = float(currency.find('ForexBuying').text)
                       eur_sell_rate = float(currency.find('ForexSelling').text)
               usd_buy_rate=usd_buy_rate;
               usd_sell_rate=usd_sell_rate;
               eur_buy_rate=eur_buy_rate;
               eur_sell_rate=eur_sell_rate;
               print("Günlük USD Kuru (Alış):", usd_buy_rate)
               print("Günlük USD Kuru (Satış):", usd_sell_rate)
               print("Günlük EURO Kuru (Alış):", eur_buy_rate)
               print("Günlük EURO Kuru (Satış):", eur_sell_rate)
           else:
               print("API'ye ulaşılamıyor. Hata kodu:", response.status_code)
               print("Günlük USD Kuru (Alış):", usd_buy_rate)
               print("Günlük USD Kuru (Satış):", usd_sell_rate)
               print("Günlük EURO Kuru (Alış):", eur_buy_rate)
               print("Günlük EURO Kuru (Satış):", eur_sell_rate)
        
        except requests.exceptions.RequestException as e:
          print("Hata oluştu:", e)
        cursor1.execute(query,usd_buy_rate,usd_sell_rate,eur_buy_rate,eur_sell_rate,str(date))
        conn2.commit()
        date += timedelta(days=1)


conn2.close()

  










