from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from math import atan,cos, sin, pi

def is_complex(user_data: str) -> bool | tuple:
    '''Функция проверяет, является ли полученное число формой записи комплексного числа вида a+bi'''
    if user_data.count('i')==1 and user_data[-1]=='i':
        user_data = user_data[:-1]
        if user_data.count('+')==1 and user_data.count('-')==0 and user_data.find('+')!=0 and user_data.find('+')!=(len(user_data)-1): # если число имеет вид a+bi
            user_data = user_data.split('+')
            if user_data[0].isdigit() and user_data[1].isdigit():
                return True
        elif user_data.count('+')==0 and user_data.count('-')==1 and user_data.find('-')!=0 and user_data.find('-')!=(len(user_data)-1): # если число имеет вид a-bi
            user_data = user_data.split('-')
            if user_data[0].isdigit() and user_data[1].isdigit():
                return True
    return False

def get_re_and_im(user_data: str) -> tuple:
    '''Функция, извлекающая действительную и мнимую часть из строкового представления комплексного числа'''
    user_data = user_data[:-1]
    if user_data.count('+')==1:
        user_data = user_data.replace('+', ' ')
    else:
        user_data = user_data.replace('-', ' ')
    user_data = user_data.split()
    return int(user_data[0]),int(user_data[1])

def get_complex_sqrt(re: int, im: int):
    '''Функция, извлекающая квадратный корень из комплексного числа с ненулевыми a и b'''
    D = (-4*re + 4*((re**2 + im**2)**0.5))/8

    sqrt_im_1 = D**0.5
    sqrt_im_2 = -D**0.5

    sqrt_re_1 = re/(2*sqrt_im_1)
    sqrt_re_2 = re/(2*sqrt_im_2)

    return f"{sqrt_re_1}+{sqrt_im_1}i",f"{sqrt_re_2}-{sqrt_im_2}i"



app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/",response_class = HTMLResponse)
def get_main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "Результат"})

@app.post("/post_num")
def get_number(request: Request, number: str = Form(...)):
    if number.isdigit() and int(number)>0:
        return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "Результат вычисления корня из вашего целого, положительного числа:", "number" : number, "result": f"Первый корень равен: {(int(number))**0.5} ; Второй корень равен: {-(int(number)**0.5)}"})
    if number.count(".")==1 and float(number)>0:
        buf = number.split(".")
        if buf[0].isdigit() and buf[1].isdigit():
            return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "Результат вычисления корня из вашего рационального, положительного числа:", "number": number, "result": f"Первый корень равен: {(float(number))**0.5} ; Второй корень равен: {-(float(number))**0.5}"})
    elif number.isdigit() and int(number)==0:
        return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "Результат вычисления корня из нуля:", "number": number, "result": f"Корень равен: {0}"})
    elif number.isdigit() and int(number)<0:
        return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "Результат вычисления корня из вашего целого, отрицательного числа:", "number": number, "result": f"Первый корень равен: {(-1*int(number))**0.5}i ; Второй корень равен: {-((-1*int(number))**0.5)}i"})
    elif number.count(".")==1 and float(number)<0:
        buf = number.split(".")
        if buf[0].isdigit() and buf[1].isdigit():
            return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "Результат вычисления корня из вашего рационального, отрицательного числа:", "number": number, "result": f"Первый корень равен: {(-1*float(number))**0.5}i ; Второй корень равен: {-((-1*float(number))**0.5)}i"})
    elif is_complex(number):
        a,b = get_re_and_im(number)
        result = get_complex_sqrt(a,b)
        return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "Результат вычисления корня из вашего комплексного числа:", "number": number, "result": f"Первый корень равен: {result[0]} ; Второй корень равен: {result[1]}"})