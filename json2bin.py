import json
import numpy as np
import cv2 as cv
import os, glob, shutil, io, base64
import PIL
from PIL import Image, ImageDraw
from threading import Thread
from multiprocessing import Process
'''
功能：
    把json文件转成label图片，
'''



class Peocess_Json():
    def __init__(self):
        # self.label = ['background', 'block_hole', 'broken_hole',
        #              'edge_flaw', 'external_residue', 'foreign_material',
        #              'pit', 'salient_point', 'unusual_surface']
        self.label = ['background', 'center']
    def img_b64_to_arr(self, img_b64):
        f = io.BytesIO()
        f.write(base64.b64decode(img_b64))
        img_arr = np.array(PIL.Image.open(f))
        return img_arr

    def img_arr_to_b64(self, img_arr):
        img_pil = PIL.Image.fromarray(img_arr)
        f = io.BytesIO()
        img_pil.save(f, format='PNG')
        img_bin = f.getvalue()
        img_b64 = base64.encodebytes(img_bin)
        return img_b64

    def read_json(self, file_path, save_path):
        with open(file_path) as f:
            json_list = json.load(f)

        shape = json_list['shapes']
        fileName = json_list['imagePath']
        fileName = fileName.split('.')[:-1]
        fileName.append('.png')
        fileName = ''.join(fileName)
        count = os.listdir(r"D:\WXWork\1688850144010912\Cache\File\2023-01\1")
        for i in range(0, len(count)):
            path = os.path.join(r"D:\WXWork\1688850144010912\Cache\File\2023-01\1", count[i])
            if json_list['imageData']:
                imageData = json_list['imageData']
            else:
                imagePath = os.path.join(os.path.dirname(path), json_list['imagePath'])
                with open(imagePath, 'rb') as f:
                    imageData = f.read()
                    imageData = base64.b64encode(imageData).decode('utf-8')



        img = self.img_b64_to_arr(imageData)
        img_h, img_w, _ = img.shape        # h,w,c

        mask = np.zeros((img_h, img_w), dtype=np.uint8)
        masks = np.zeros((img_h, img_w), dtype=np.uint8)
        for i in range(len(shape)):


            label = shape[i]['label']
            if label not in self.label:
                self.label.append(label)
            index = self.label.index(label)
            # index = 255
            points = shape[i]['points']
            masks = self.polygons_to_mask(mask, polygons=points, index=index) + masks
        cv.imwrite('{}/{}'.format(save_path,fileName), masks)


    def polygons_to_mask(self, mask, polygons, index):
        mask = PIL.Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        mask = np.where(mask, index, 0)
        return mask
        

class MyProcess(Process):
    def __init__(self):
        super(MyProcess, self).__init__()

    def run(self) -> None:
        self.js = Peocess_Json()
        self.js.read_json(self.path, self.save_path)

    def getPath(self, path, save_p):
        self.path = path
        self.save_path = save_p

if __name__ == '__main__':
    '''
    解析json文件代码，参数有2个：
    1、read_json_file_path：按一下格式填入 json文件所在文件夹位置
    2、save_mask_file_path：按一下格式填入mask图保存位置
    '''
    FLAG = False # 是否使用多进程
    read_json_file_path = r'D:\WXWork\1688850144010912\Cache\File\2023-01\1\*.json'
    save_mask_file_path = r'D:\WXWork\1688850144010912\Cache\File\2023-01\1\Annotations'
    json_files = glob.glob(read_json_file_path)
    for i in json_files:
        print(i)
        if FLAG:
            myThread = MyProcess()
            myThread.getPath(i, save_mask_file_path)
            myThread.start()
        else:
            js = Peocess_Json()
            js.read_json(i, save_mask_file_path )



