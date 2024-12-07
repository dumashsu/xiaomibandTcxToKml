"""
小米手環匯出KML 再轉成 Google Map 可用的 KML
"""

from bs4 import BeautifulSoup
import sys
def main(v_argv):
    if len(v_argv)==1:
        print("Usage:python XaioMiBandKmlToKml.py <filename kml>")
        sys.exit()    
    #開參數檔並讀入 v_ini_data 內,轉出時可直接使用,簡化程式
    with open('xiiomiband.ini', 'r') as kml_f:
        v_ini_data=kml_f.read()
    with open('01.kml', 'r') as f:
        s = BeautifulSoup(f, 'xml')
        with open('out.kml', 'w') as writer:
            """
            取各位置好取出字串
            Head 1404
            Tack Points的起點 1527
            Track Points的終點 1706
            Track Points的    1930
            將轉出的KML檔內的名稱替換
            寫入抬頭-至起點, 寫入時才改名稱才不會 ID 錯誤
            """
            writer.write(v_ini_data[0:1527].replace("Track Points","02"))
            v_first_data=True
            v_coordinates_content=v_coordinates_data=""
            #第一筆直接寫入檔案,其它則加入 v_coordinates_content , 最後才一起寫入
            #目的是要取第一筆和最後一筆的座標
            for coords in s.find_all('coordinates'):
                v_coordinates_data='\n'+' '*10+coords.string
                if v_first_data:
                    writer.write(v_coordinates_data)
                    v_first_data=False
                else:                  
                    v_coordinates_content=v_coordinates_content+v_coordinates_data                   
            # 寫入終點和其值
            writer.write(v_ini_data[1527:1706].replace("Track Points","02"))
            writer.write(v_coordinates_data)
            writer.write(v_ini_data[1706:1930].replace("Track Points","02"))
            #去除最後一段位置後寫入GPS
            writer.write(v_coordinates_content[:-len(v_coordinates_data)])
            #寫檔尾
            writer.write('\n'+v_ini_data[1931:])
if __name__ == "__main__":
    main(sys.argv)
