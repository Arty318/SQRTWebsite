from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from math import atan,cos, sin, pi

def is_complex(user_data: str) -> bool | tuple:
    if user_data.count('i')==1 and user_data[-1]=='i':
        user_data = user_data[:-1]
        if user_data.count('+')==1 and user_data.count('-')==0 and user_data.find('+')!=0 and user_data.find('+')!=(len(user_data)-1):
            user_data = user_data.split('+')
            if user_data[0].isdigit() and user_data[1].isdigit():
                return True
        elif user_data.count('+')==0 and user_data.count('-')==1 and user_data.find('-')!=0 and user_data.find('-')!=(len(user_data)-1):
            user_data = user_data.split('-')
            if user_data[0].isdigit() and user_data[1].isdigit():
                return True
    return False

def get_re_and_im(user_data: str) -> tuple:
    user_data = user_data[:-1]
    if user_data.count('+')==1:
        user_data = user_data.replace('+', ' ')
    else:
        user_data = user_data.replace('-', ' ')
    user_data = user_data.split()
    return int(user_data[0]),int(user_data[1])

def get_complex_sqrt(re: int, im: int):
    r = (re**2 + im**2)**0.5
    phi = atan(im / re)


    result_re_1 = str((r**0.5)*(cos(phi/2)))
    result_im_1 = str((r**0.5)*(sin(phi/2)))

    result_re_2 = str((r**0.5)*(cos((phi+2*pi)/2)))
    result_im_2 = str((r**0.5)*(sin((phi+2*pi)/2)))

    if result_im_1[0] == '-':
        result_complex_1 = "Первый корень = " + result_re_1 + result_im_1 + 'i'
    else:
        result_complex_1 = "Первый корень = " + result_re_1 + '+' + result_im_1 + 'i'

    if result_im_2[0] == '-':
        result_complex_2 = "Второй корень = " + result_re_2 + result_im_2 + 'i'
    else:
        result_complex_2 = "Второй корень = " + result_re_2 + '+' + result_im_2 + 'i'

    return result_complex_1, result_complex_2





app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/",response_class = HTMLResponse)
def get_main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "Результат"})

@app.post("/post_num")
def get_number(request: Request, number: str = Form(...)):
    if is_complex(number):
        re_and_im = get_re_and_im(number)
        print("Квадратный корень из вашего комплексного числа:" , get_complex_sqrt(*re_and_im))
        return templates.TemplateResponse("index.html", {"request": request, "number": number, "result": get_complex_sqrt(*re_and_im), "type_of_result": "Квадратный корень из вашего комплексного числа"})
    else:
        arifm_sqrt = int(number)**0.5
        print("Квадратный корень из вашего числа:", arifm_sqrt)
        return templates.TemplateResponse("index.html", {"request": request, "number": number, "result": arifm_sqrt, "type_of_result": "Квадратный корень из вашего числа"})


