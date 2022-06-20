"""
«Антивирус». Программа запоминает содержимое указанной папки и длину
файлов в ней. При запуске она определяет появление новых файлов в
данной папке, удаление существовавших и изменение размера у исполняемых
файлов. Выводится информация об изменениях. Количество анализируемых
папок не ограничено.
"""

from tkinter import * # модуль графического интерфейса
import tkinter.filedialog # модуль файлового диалога 
import os # модуль для взаимодействия с файловой системой
import ast # модуль, используемый для преобразования строки в список

def Folderpath(): # функция выбора директории
    
    entry.delete(0, END)
    entry.insert(0, tkinter.filedialog.askdirectory())


def DifferencesCheck(array): # функция вывода изменений в директории
    #ray - новые данные ### #array - данные в базе
    ray=os.listdir(path=entry.get())
    for i in range(len(ray)):
        ray[i]=[ray[i]] # преобразование 1мерного в 2мерный массив
        ray[i].append(os.path.getsize(entry.get()+"/"+ray[i][0])) # размер файла в байтах

    array=ast.literal_eval(array) # преобразование строки из базы в список

    text['state'] = "normal"
    text.insert(END, "Выполняется проверка папки " + entry.get() + "\n")
    
    text.insert(END, "Изменение размеров содержимого: ") 
    b=0
    for i in ray:#поиск изменённых файлов
        for j in array:
            if i[0]==j[0] and i[1]!=j[1]: #сравнение размеров файлов в байтах
                b=1
                text.insert(END,"\n " + i[0] + ": " + str(j[1]) + " b → " + str(i[1]) + " b", "tag_blue_text")           
    if b==0:
        text.insert(END,"не выявлено\n", "tag_green_text")

  
    
    names1=[] # новый список с именами файлов из базы
    names2=[] # новый список с именами проверяемых файлов
    for i in array:
        names1.append(i[0])
    for i in ray:
        names2.append(i[0])
    
    plus_names = list(set(names2) - set(names1)) # новые файлы
    minus_names = list(set(names1) - set(names2)) # удалённые файлы
    
    if plus_names == [] and minus_names==[]:
        text.insert(END,"Изменение содержимого: ")
        text.insert(END,"не выявлено\n", "tag_green_text")
   
    if plus_names != []:
        text.insert(END, "\nНовые файлы:\n")
        for i in plus_names:
            text.insert(END, i + "\n", "tag_blue_text")
            
    if minus_names != []:
        text.insert(END, "\nУдалённые файлы:\n")
        for i in minus_names:
            text.insert(END, i + "\n", "tag_blue_text")
        
    text.insert(END, "\n")
    text['state'] = "disabled" 
        
def ExistingFile(): # функция поиска папки в базе
    
    b=0
    f = open('logs.txt', 'r')
    for line in f: 
        if b:
            DifferencesCheck(line)
            break
        if line==entry.get()+"\n": #имя папки есть в базе
            b=1
    f.close()

        
def NewFile(): # функция добавления папки в базу

    f = open('logs.txt', 'a') # запись текущего содержимого папки
    arr=os.listdir(path=entry.get()) # список файлов в папке
    for i in range(len(arr)):
        arr[i]=[arr[i]] # преобразование 1мерного в 2мерный список
        arr[i].append(os.path.getsize(entry.get()+"/"+arr[i][0])) # размер файла в байтах
        
    f.write("\n\n"+ entry.get() + "\n" + str(arr)) # запись информации
    f.close()
    
    text['state'] = "normal"
    text.insert(END, 'Папка добавлена в базу\n')
    text['state'] = "disabled"
    
def Start(): # функция проверки папки

    f = open('logs.txt', 'a') 
    if os.path.exists(entry.get()):
        f = open('logs.txt', 'r') 
        b=0
        for line in f: # проверка папки на содержание в базе
            if line == entry.get()+"\n":
                b = 1
                break
        if b:
            ExistingFile()
        else:
            NewFile()        
    else:
        text['state'] = "normal"
        text.insert(END, 'Путь к папке указан некорректно\n', 'tag_red_text')
        text['state'] = "disabled"
    f.close()
            
    
    
root = Tk()
root.resizable(0, 0)
root.geometry('600x450')
root.title('Курсовая работа Богданов Максим 19-ИЭ-1')



c = Canvas(width = 596, height = 446, bg = 'grey') # канва
c.place(x = 0, y = 0) 

entry = Entry(width = 55, font = "Verdana 11") # поле ввода
entry.place(x = 20, y = 50)

text = Text(width = 68, height = 18, font = "Verdana 10", state='disabled') # поле вывода информации
text.place(x = 18, y = 120)
text.tag_config('tag_red_text', foreground='red')
text.tag_config('tag_green_text', foreground='green')
text.tag_config('tag_blue_text', foreground='blue')

search = Button(width = 6, text = "Обзор", font = "Verdana 9", command = Folderpath) # выбор папки
search.place(x = 30, y = 80)

enter = Button(width = 6, text = "Enter", font = "Verdana 9", command = Start) # начать сканирование
enter.place(x = 110, y =80)

label = Label(text = "Выберите папку для сканирования", bg = "lightgrey", font = "Verdana 11") # метка
label.place(x = 18, y = 16)

root.mainloop()

