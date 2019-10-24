#!/usr/bin/env python
# coding: utf-8

# In[42]:

import requests 
import os,sys,shutil
import datetime
import zipfile
import logging

sys.stdout.write('Запущен процесс переноса версии Preferentum с http://172.28.0.247:81/\n')


dev_serv='http://172.28.0.247:81/'
modules=['web','db','loader','manager','service']
versions_path='C:\\Users\\Администратор\\Downloads\\Preferentum_versions'
preferentum_path='C:\\Distr\\Preferentum1\\'
config_path='C:\\Users\\Администратор\\Downloads\\Preferentum_versions\\configs\\'
pref_files=os.listdir(preferentum_path)
logging.basicConfig(filename='C:\\Distr\\py_log.log', level=logging.INFO)

if len(pref_files)==0:
	logging.info(now+'Исходная папка пуста\n')
	sys.stdout.write('Исходная папка пуста\n')
#     exit()

else:
    now=datetime.datetime.today().strftime('%d.%m.%Y %H.%M')
    try:
        sys.stdout.write('Запущен процесс сборки новой версии платформы\n')
        makeNewVersion=requests.get(dev_serv+'admin/archive')
        sys.stdout.write(makeNewVersion.text+'\n')
        sys.stdout.write('Новый релиз платформы собран\n')
    except: 
		logging.info(now+'Невозможно собрать новый релиз платформы\n')
		sys.stdout.write('Невозможно собрать новый релиз платформы\n')

    try : 
        sys.stdout.write('Создаем папку для переноса старой версии\n')
        dirname=versions_path+'\\Preferentum '+now
        os.mkdir(dirname)
        sys.stdout.write('Папка для переноса старой версии успешно создана\n')
    except:
		logging.info(now+'Невозможно создать папку\n')
		sys.stdout.write('Невозможно создать папку\n')
		
    try:
        sys.stdout.write('Начинаем процесс переноса старых файлов\n')
        for file in pref_files:
            shutil.move(preferentum_path+file, dirname+'\\'+file)
        sys.stdout.write('Процесс переноса старых файлов успешно заверешен\n')
    except :
		logging.info(now+'Невозможно перенести файлы\n')
		sys.stdout.write('Невозможно перенести файлы\n')
            
    try:
        sys.stdout.write('Скачиваем архивы модулей новой версии\n')
        for module in modules:
            f=open(preferentum_path+module+'.zip','wb') #открываем файл для записи, в режиме wb
            dwnldf=requests.get(dev_serv+module+'.zip') #делаем get  запрос
            f.write(dwnldf.content) #записываем содержимое в файл content запроса
            f.close()
        sys.stdout.write('Архивы успешно загружены\n')
    except :
		logging.info(now+'Невозможно скачать файлы\n')
		sys.stdout.write('Невозможно скачать файлы\n')
        
    try:  
        sys.stdout.write('Начинаем процесс разархивации\n')
        for file in pref_files:
            zip_ref = zipfile.ZipFile(preferentum_path+file, 'r')
            zip_ref.extractall(preferentum_path+file[:-4])
            zip_ref.close()
        sys.stdout.write('Процесс разархивации успешно выполнен\n')
    except :
		logging.info(now+'Невозможно разархивировать файлы\n')
		sys.stdout.write('Невозможно разархивировать файлы\n')
		
    try :
        sys.stdout.write('Переносим конфиги\n')
        for module in modules:
            if module !='db':
                config_file=os.listdir(config_path+module)
                print("Переносим "+config_file[0])
                shutil.copy2(config_path+module+'\\'+config_file[0], preferentum_path+module+'\\')
        sys.stdout.write('Конфиги успешно перенесены\n')
    except :
		logging.info(now+'Невозможно перенести конфиги\n')
		sys.stdout.write('Невозможно перенести конфиги\n')              
sys.stdout.write('Процесс переноса версии Preferentum с http://172.28.0.247:81/ успешно завершен\n')


