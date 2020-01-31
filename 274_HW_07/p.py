import shutil
import PyPDF2
from PIL import Image
import pytesseract
import time
import os
from pymongo import MongoClient

def  Connect_collectionsDB(col_name):
    res = None
    client = MongoClient('localhost',27017)
    db = client['SCALE_INFO']
    try:
       res = db.create_collection(col_name)
    except:
       print('!!!')
       res= db.get_collection(col_name)
    return res

def Write_to_collections(col_con, list_of_vac):
    col_con.insert_one(list_of_vac)

# todo Отсортировать файлы jpg и pdf
def Read_files_by_type(dir, type_files = []) :
    list_of_files = []
    folder = []
    #print('type_files', type_files)
    for i in os.walk(dir) :
        folder.append(i)
    #print('folder',folder)
    for address, dirs, files in folder:
        for file in files:
            if type_files  != []:
                for tf in type_files :
                    #print(tf)
                    #print(file[file.rfind('.'):])
                    if file.lower().rfind('.'+tf)  != -1 :
                        fname = (address+'\\', file)
                        list_of_files.append(fname)
            else:
                fname = (address, file)
                list_of_files.append(fname)
    return list_of_files
# todo Извлечь jpg из pdf и сохранить в папке изображений
def extract_pdf_image(pdf_path):
    try:
        pdf_file = PyPDF2.PdfFileReader(open(pdf_path, "rb"), strict=False)
    except PyPDF2.utils.PdfReadError as e:
        return None
    except FileNotFoundError as e:
        return None
    result = []
    for page_num in range(0, pdf_file.getNumPages()):
        page = pdf_file.getPage(page_num)
        page_obj = page['/Resources']['/XObject'].getObject()
        if page_obj['/Im0'].get('/Subtype') == "/Image":
            size = (page_obj['/Im0']['/Width'], page_obj['/Im0']['/Height'])
            data = page_obj['/Im0']._data
            if page_obj['/Im0']['/ColorSpace'] == '/DeviceRGB':
                mode = 'RGB'
            else:
                mode = 'P'
            if page_obj['/Im0']['/Filter'] == '/FlateDecode':
                file_type = 'png'
            elif page_obj['/Im0']['/Filter'] == '/DCTDecode':
                file_type = 'jpg'
            elif page_obj['/Im0']['/Filter'] == '/JPXDecode':
                file_type = 'jp2'
            else:
                file_type = 'bmp'
            result_strict = {
                'page': page_num,
                'size': size,
                'data': data,
                'mode': mode,
                'file_type': file_type,
            }
            result.append(result_strict)
    return result

def save_pdf_image(file_name, f_path, *pdf_strict):
    for item in pdf_strict:
        name = f"{file_name}_#_{item['page']}.{item['file_type']}"
        with open(f"{f_path}/{name}", "wb") as image:
            image.write(item['data'])

# todo не забыть про формат имен файлов

# todo Извлеч номер кассы из поля

def extract_number(file_path):
    img_obj = Image.open(file_path)
    ims = img_obj.size
    if ims[0]<ims[1]:
        img_obj = img_obj.rotate(90, expand=True) #, center=True, translate=None, fillcolor=None)
    #print(1)
    text = pytesseract.image_to_string(img_obj, 'rus')
    pattern = 'заводской (серийный) номер'
    pattern2 = 'заводской номер'
    pattern3 = "(номерa)"
    pattern4 = "при наличии"
    result = []
    for idx, line in enumerate(text.split('\n')):
        #print('idx= ',idx,'line= ', line)
        lt= line.lower()
        if (lt.find(pattern2) + 1 or lt.find(pattern) + 1) and lt.find(pattern4) == -1: #or line.lower().find(pattern3) + 1:
            eng_text = pytesseract.image_to_string(img_obj, 'eng')
            str_num = eng_text.split('\n')[idx]
            number = eng_text.split('\n')[idx].split(' ')[-1]
            result.append(number)
            print(number)
            print(str_num)
            print(line)
            print('--'*30)

    # todo при отсутсвии распознавания вернуть соответсвующее сообщение или error
    return result

# todo сохранить все в БД MONGO


if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    pdf_file_path = 'data_for_parse/8416_4.pdf'
    file_name = '8416_4'
    image_path = "data_for_parse/image"
    img_file_path = 'data_for_parse/image/16.03.2019  (2).jpg'
    dir = 'data_for_parse'
    type_files= ['pdf', 'jpg']
    list_of_file = Read_files_by_type(dir, ['pdf', 'jpg'])
    print('Всего файлов',len(list_of_file))
    list_pdf = []
    list_jpg = []
    for dir, file in list_of_file:
        ext = file[file.rfind(".") + 1:]
        if ext == 'pdf':
            list_pdf.append({'dir': dir, 'name': file})
        elif ext == 'jpg':
            list_jpg.append({'dir': dir, 'name': file})
        else:
            pass

    print('Всего  pdf файлов', len(list_pdf))
    print('Всего  jpg файлов', len(list_jpg))

    col = Connect_collectionsDB('Scale id')
    # pdf_result = extract_pdf_image(pdf_file_path)
    # save_pdf_image(file_name, image_path, *pdf_result)
    for file in list_jpg:
        fn= f'{file["dir"]}\\{file["name"]}'
        print('<<>>'*15)
        print(fn)
        print('--' * 30)
        res = extract_number(fn)#img_file_path)
        res_by_file = {'file':fn, 'result':res}
        Write_to_collections(col, res_by_file)
    print(1)
