import os
import time
import re
from datetime import datetime

from PIL import ImageGrab, Image, ImageEnhance
import pyocr

basedir = os.path.abspath(os.path.dirname(__file__))

# Path設定
TESSERACT_PATH = 'C:\Program Files\Tesseract-OCR' #インストールしたTesseract-OCRのpath

if TESSERACT_PATH not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + TESSERACT_PATH

#OCRエンジン取得
tools = pyocr.get_available_tools()
tool = tools[0]

#OCRの設定
builder = pyocr.builders.TextBuilder()

areas = ['北海道','青森','岩手','宮城','秋田','山形','福島','茨城','栃木','群馬',
        '埼玉','千葉','東京','神奈川','新潟','富山','石川','福井','山梨','長野',
        '岐阜','静岡','愛知','三重','滋賀','京都','大阪','兵庫','奈良','和歌山',
        '鳥取','島根','岡山','広島','山口','徳島','香川','愛媛','高知','福岡',
        '佐賀','長崎','熊本','大分','宮崎','鹿児島','沖縄',
        '札幌','仙台','さいたま','横浜','川崎','相模原','浜松','名古屋','堺','神戸','北九州']

def screen_capture(seconds):
    file_paths = []
    for i in range(seconds):
        screenshots = ImageGrab.grab()
        dt_now = datetime.now().strftime('%Y%m%d-%H%M%S')    
        file_path = os.path.join(basedir, 'screen_img', f'screen{dt_now}.png')
        screenshots.save(file_path)
        file_paths.append(file_path)
        time.sleep(1)
    return file_paths

def read_area_text(file_path):
    img = Image.open(file_path)
    img_g = img.convert('L') #Gray変換
    enhancer= ImageEnhance.Contrast(img_g) #コントラストを上げる
    img_con = enhancer.enhance(2.0) #コントラストを上げる
    txt_pyocr = tool.image_to_string(img_con , lang='jpn', builder=builder)  #画像からOCRで日本語を読んで、文字列として取り出す
    words = re.split(r'\s+', txt_pyocr) 
    f = open(f'screen_cap.txt', 'a', encoding='utf-8')
    for word in words:
        for area in areas:
            if area in word:
                f.write(f'{os.path.basename(file_path)}:{word}\n')
    f.close()


file_paths = screen_capture(60)
for file_path in file_paths:
     read_area_text(file_path)


