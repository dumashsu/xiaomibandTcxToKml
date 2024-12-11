"""
小米手環匯出 TCX  再轉成 Google Map 可用的 KML
Id : 起始日期/時間 s.find('Id').get_text()[:10]
Calories: 卡路里, 有2 個 前為總 後為最後一次(有暫停) s.select('Calories'[0].get_text())
TotalTimeSeconds: 總時間 s.find('TotalTimeSeconds').get_text()
DistanceMeters: 距離公分 s.find("DistanceMeters").get_text() cm
HeartRateBpm: 平均心率 s.find("HeartRateBpm").get_text()
Steps: 步數 s.find("Steps").get_text()
Trackpoint: 時間/經緯度, 經度和緯度 需調換才會是正確順序
        Time: 時間
        Position: 經度
        LatitudeDegrees: 緯度
"""

from bs4 import BeautifulSoup
import sys

def main(v_argv):
    if len(v_argv)==1:
        print("Usage:python XaioMiBandTcxToKml.py <filename tcx>")
        sys.exit()
    #開參數檔並讀入 v_ini_data 內,轉出時可直接使用,簡化程式
    #v_argv=["1",v_argv]
    with open('xiaomiband.ini', 'r') as kml_f:
        v_ini_data=kml_f.read()
    with open(v_argv[1]+'.tcx', 'r') as f:
        s = BeautifulSoup(f, 'xml')
        with open(v_argv[1]+'.kml', 'w') as writer:
            """
            取各位置好取出字串
            Head 1404           
            Tack Points的起點描述在 1456    起點座標 1527
            Track Points的終點座標 1706
            Track Points的描述在  1810  而座標    1930
            將轉出的KML檔內的名稱替換
            寫入抬頭-至起點, 寫入時才改名稱才不會 ID 錯誤
            """
            writer.write(v_ini_data[0:1527].replace("Track Points",v_argv[1]))
            #第一筆直接寫入檔案,其它則加入 v_coordinates_content , 最後才一起寫入
          
            v_first_data=True
            v_coordinates_content=v_coordinates_data=""
            #目的是要取第一筆和最後一筆的座標
            for coords in s.find_all('Trackpoint'):
                #將值取出
                v_str=coords.get_text(',').split(',')
                v_coordinates_data='\n'+' '*12+v_str[2]+','+v_str[1]
                if v_first_data:
                    writer.write(v_coordinates_data)
                    v_first_data=False
                else:                  
                    v_coordinates_content=v_coordinates_content+v_coordinates_data                   
            # 寫入終點和其值
            writer.write(v_ini_data[1527:1706].replace("Track Points",v_argv[1]))
            writer.write(v_coordinates_data)
            writer.write(v_ini_data[1706:1810].replace("Track Points",v_argv[1]))
            
            #寫入描述
            writer.write(" "*6+"<description>\n"+" "*8+"<![CDATA[")
            writer.write("日期: "+s.find('Id').get_text()[:10]+"<br>")
            #卡路里有2個第一個為總，第2個為實際
            v_Calories = s.find_all('Calories')
            writer.write("消耗卡路里: "+v_Calories[0].get_text()+"/"+v_Calories[1].get_text()+"<br>")
            writer.write("時間: "+s.find('TotalTimeSeconds').get_text()+"<br>")
            v_DistanceMeters=s.find("DistanceMeters").get_text()        
            writer.write("距離: "+v_DistanceMeters[:-3]+'.'+v_DistanceMeters[-3:]+" KM<br>")
            writer.write("平均心率: "+s.find("HeartRateBpm").get_text()+"<br>")
            writer.write("步數:  "+s.find("Steps").get_text()+"<br>")
            writer.write(" ]]>\n"+" "*6+"</description>")       
            
            #去除最後一段位置後寫入GPS
            writer.write('\n'+v_ini_data[1811:1930:])
            writer.write(v_coordinates_content[:-len(v_coordinates_data)])
            #寫檔尾
            writer.write('\n'+v_ini_data[1931:])
            
if __name__ == "__main__":
    main(sys.argv)
    #main("20241210徒步")
