import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from math import atan,cos, sin, pi

def is_complex(user_data: str) -> bool | tuple:
    '''Функция проверяет, является ли полученное число формой записи комплексного числа вида a+bi'''
    if user_data=='i':                                                                                                                                              # Если было введено i
        return True
    if user_data=='-i':                                                                                                                                             # Если было введено -i
        return True
    if user_data.count('i')==1 and user_data[-1]=='i':
        user_data = user_data[:-1]
        if user_data.count('+')==1 and user_data.count('-')==0 and user_data.find('+')!=0 and user_data.find('+')!=(len(user_data)):                                # Если число имеет вид a+bi
            user_data = user_data.split('+')
            if user_data[0].count('.')!=0:

                if (user_data[0].find('.')!=0) and (user_data[0].find('.')!=(len(user_data[0])-1)) and (user_data[0].count('.')==1):

                    user_data[0] = user_data[0].replace('.','')

                else:
                    return False
            if user_data[1].count('.')!=0:
                if user_data[1].find('.')!=0 and user_data[1].find('.')!=(len(user_data[1])-1) and user_data[1].count('.')==1:
                    user_data[1] = user_data[1].replace('.','')
                else:
                    return False
            if (user_data[0].isdigit() and user_data[1].isdigit()) or (user_data[0].isdigit and user_data[1]==''):

                return True


        if user_data.count('+')==1 and user_data.count('-')==1 and user_data.find('+')!=0 and user_data.find('+')!=(len(user_data)) and user_data[0]=='-':           # Если число имеет вид -a+bi
            user_data = user_data[1:].split('+')
            if user_data[0].count('.')!=0:
                if (user_data[0].find('.')!=0) and (user_data[0].find('.')!=(len(user_data[0])-1)) and (user_data[0].count('.')==1):

                    user_data[0] = user_data[0].replace('.','')
                else:
                    return False
            if user_data[1].count('.')!=0:
                if user_data[1].find('.')!=0 and user_data[1].find('.')!=(len(user_data[1])-1) and user_data[1].count('.')==1:
                    user_data[1] = user_data[1].replace('.','')
                else:
                    return False
            if (user_data[0].isdigit() and user_data[1].isdigit()) or (user_data[0].isdigit and user_data[1]==''):
                return True


        if user_data.count('+')==0 and user_data.count('-')==1 and user_data.find('-')!=0 and user_data.find('-')!=(len(user_data)):                                   # Если число имеет вид a-bi
            user_data = user_data.split('-')
            if user_data[0].count('.')!=0:
                if user_data[0].find('.')!=0 and user_data[0].find('.')!=(len(user_data[0])-1) and user_data.count('.')==1:
                    user_data[0] = user_data[0].replace('.','')
                else:
                    return False
            if user_data[1].count('.')!=0:
                if user_data[1].find('.')!=0 and user_data[1].find('.')!=(len(user_data[1])-1) and user_data.count('.')==1:
                    user_data[1] = user_data[1].replace('.','')
                else:
                    return False
            if (user_data[0].isdigit() and user_data[1].isdigit()) or (user_data[0].isdigit and user_data[1]==''):
                return True


        if user_data.count('+')==0 and user_data.count('-')==2 and user_data[0]=='-' and user_data[1:].find('-')!=0 and user_data[1:].find('-')!=(len(user_data[1:])): # Если число имеет вид -a-bi
            user_data = user_data[1:].split('-')
            if user_data[0].count('.')!=0:
                if user_data[0].find('.')!=0 and user_data[0].find('.')!=(len(user_data[0])-1) and user_data.count('.')==1:
                    user_data[0] = user_data[0].replace('.','')
                else:
                    return False
            if user_data[1].count('.')!=0:
                if user_data[1].find('.')!=0 and user_data[1].find('.')!=(len(user_data[1])-1) and user_data.count('.')==1:
                    user_data[1] = user_data[1].replace('.','')
                else:
                    return False
            if (user_data[0].isdigit() and user_data[1].isdigit()) or (user_data[0].isdigit and user_data[1]==''):
                return True


        if user_data[0].isdigit(): # число вида bi
            if user_data.count('.')==1 and user_data.find('.')!=0 and user_data.find('.')!=(len(user_data)-1):
                user_data = user_data.replace('.','')

            if user_data.isdigit():
                return True


        if user_data[0]=='-': # число вида -bi
            if user_data.count('.')==1 and user_data.find('.')!=0 and user_data.find('.')!=(len(user_data)-1):
                user_data = user_data.replace('.','')
            if user_data[1:].isdigit():
                return True


    return False

def get_re_and_im(user_data: str) -> tuple:
    '''Функция, извлекающая действительную и мнимую часть из строкового представления комплексного числа'''
    if user_data=='i': # если введено просто i
        return float(0),float(1)
    if user_data=='-i':
        return float(0),-float(1)
    user_data = user_data[:-1]
    if user_data[0].isdigit(): # если введенно 15i
        if user_data.isdigit():
            return float(0),float(user_data)
        if user_data.count('.')==1:
            spisok = user_data.split('.')
            if spisok[0].isdigit() and spisok[1].isdigit():
                return float(0),float(user_data)


    if user_data[0]=='-': # если введенно -15i
        if user_data[1:].isdigit():
            return float(0),float(user_data)
        if user_data.count('.')==1:
            spisok = user_data.split('.')
            if spisok[0][1:].isdigit() and spisok[1].isdigit():
                return float(0),float(user_data)



    if user_data[0].isdigit(): # ЕСЛИ ДЕЙСТВИТЕЛЬНАЯ ЧАСТЬ С ПЛЮСОМ
        if user_data.count('+')==1: # ЕСЛИ МНИМАЯ ЧАСТЬ С ПЛЮСОМ
            user_data = user_data.split('+')
            print(user_data)
            if (user_data[1])=='':
                return float(user_data[0]),float(1)
            else:
                return float(user_data[0]),float(user_data[1])
        else:                      # ЕСЛИ МНИМАЯ ЧАСТЬ С МИНУСОМ
            user_data = user_data.split('-')
            if (user_data[1])=='':
                return float(user_data[0]),-float(1)
            else:
                return float(user_data[0]),-float(user_data[1])
    else:                         # ЕСЛИ ДЕЙСТВИТЕЛЬНАЯ ЧАСТЬ С МИНУСОМ
        if user_data.count('+')==1: # ЕСЛИ МНИМАЯ ЧАСТЬ С ПЛЮСОМ
            user_data = user_data[1:].split('+')
            if (user_data[1])=='':
                return -float(user_data[0]),float(1)
            else:
                return -float(user_data[0]),float(user_data[1])
        else:                     # ЕСЛИ МНИМАЯ ЧАСТЬ С МИНУСОМ
            user_data = user_data[1:].split('-')
            if (user_data[1])=='':
                return -float(user_data[0]),-float(1)
            else:
                return -float(user_data[0]),-float(user_data[1])


def get_complex_sqrt(re: int, im: int, precision: str)->tuple:
    '''Функция, извлекающая квадратный корень из комплексного числа с ненулевыми a и b'''
    print(re,im)
    if re==0:
        print(1)
        if im>0:
            D = (-4 * 0 + 4 * ((0 ** 2 + 1 ** 2) ** 0.5)) / 8

            sqrt_im_1 = D ** 0.5
            sqrt_im_2 = -D ** 0.5

            sqrt_re_1 = 1 / (2 * sqrt_im_1)
            sqrt_re_2 = 1 / (2 * sqrt_im_2)

            real_of_sqrt1 = (im**0.5)*sqrt_re_1
            im_of_sqrt1 = (im**0.5)*sqrt_im_1
            real_of_sqrt2 = (im**0.5)*sqrt_re_2
            im_of_sqrt2 = (im**0.5)*sqrt_im_2

            if all(x=='0' for x in str(real_of_sqrt1)[str(real_of_sqrt1).find('.')+1:]):
                real_of_sqrt1 = int(real_of_sqrt1)

            if all(x=='0' for x in str(real_of_sqrt2)[str(real_of_sqrt2).find('.')+1:]):
                real_of_sqrt2 = int(real_of_sqrt2)

            if all(x=='0' for x in str(im_of_sqrt1)[str(im_of_sqrt1).find('.')+1:]):
                im_of_sqrt1 = int(im_of_sqrt1)

            if all(x=='0' for x in str(im_of_sqrt2)[str(im_of_sqrt2).find('.')+1:]):
                im_of_sqrt2 = int(im_of_sqrt2)

            if '.00000000' in str(real_of_sqrt1):
                real_of_sqrt1 = int(str(real_of_sqrt1)[:str(real_of_sqrt1).find('.')])
            if '.00000000' in str(real_of_sqrt2):
                real_of_sqrt2 = int(str(real_of_sqrt2)[:str(real_of_sqrt2).find('.')])
            if '.00000000' in str(im_of_sqrt1):
                im_of_sqrt1 = int(str(im_of_sqrt1)[:str(im_of_sqrt1).find('.')])
            if '.00000000' in str(im_of_sqrt2):
                im_of_sqrt2 = int(str(im_of_sqrt2)[:str(im_of_sqrt2).find('.')])

            if '.99999999' in str(real_of_sqrt1):
                real_of_sqrt1 = int(str(real_of_sqrt1)[:str(real_of_sqrt1).find('.')])+1
            if '.99999999' in str(real_of_sqrt2):
                real_of_sqrt2 = int(str(real_of_sqrt2)[:str(real_of_sqrt2).find('.')])+1
            if '.99999999' in str(im_of_sqrt1):
                im_of_sqrt1 = int(str(im_of_sqrt1)[:str(im_of_sqrt1).find('.')])+1
            if '.99999999' in str(im_of_sqrt2):
                im_of_sqrt2 = int(str(im_of_sqrt2)[:str(im_of_sqrt2).find('.')])+1

            return f"{real_of_sqrt1:.{precision}f}+{im_of_sqrt1:.{precision}f}i",f"{real_of_sqrt2:.{precision}f}{im_of_sqrt2:.{precision}f}i"
        if im<0:
            D = (-4 * 0 + 4 * ((0 ** 2 + 1 ** 2) ** 0.5)) / 8

            sqrt_im_1 = D ** 0.5
            sqrt_im_2 = -D ** 0.5

            sqrt_re_1 = 1 / (2 * sqrt_im_1)
            sqrt_re_2 = 1 / (2 * sqrt_im_2)

            real_of_sqrt1 = -1*((-im)**0.5)*sqrt_re_1
            real_of_sqrt2 = -1*((-im)**0.5)*sqrt_re_2
            im_of_sqrt1 = sqrt_im_1*((-im)**0.5)
            im_of_sqrt2 = sqrt_im_2*((-im)**0.5)

            if all(x=='0' for x in str(real_of_sqrt1)[str(real_of_sqrt1).find('.')+1:]):
                real_of_sqrt1 = int(real_of_sqrt1)

            if all(x=='0' for x in str(real_of_sqrt2)[str(real_of_sqrt2).find('.')+1:]):
                real_of_sqrt2 = int(real_of_sqrt2)

            if all(x=='0' for x in str(im_of_sqrt1)[str(im_of_sqrt1).find('.')+1:]):
                im_of_sqrt1 = int(im_of_sqrt1)

            if all(x=='0' for x in str(im_of_sqrt2)[str(im_of_sqrt2).find('.')+1:]):
                im_of_sqrt2 = int(im_of_sqrt2)

            if '.00000000' in str(real_of_sqrt1):
                real_of_sqrt1 = int(str(real_of_sqrt1)[:str(real_of_sqrt1).find('.')])
            if '.00000000' in str(real_of_sqrt2):
                real_of_sqrt2 = int(str(real_of_sqrt2)[:str(real_of_sqrt2).find('.')])
            if '.00000000' in str(im_of_sqrt1):
                im_of_sqrt1 = int(str(im_of_sqrt1)[:str(im_of_sqrt1).find('.')])
            if '.00000000' in str(im_of_sqrt2):
                im_of_sqrt2 = int(str(im_of_sqrt2)[:str(im_of_sqrt2).find('.')])

            if '.99999999' in str(real_of_sqrt1):
                real_of_sqrt1 = int(str(real_of_sqrt1)[:str(real_of_sqrt1).find('.')])+1
            if '.99999999' in str(real_of_sqrt2):
                real_of_sqrt2 = int(str(real_of_sqrt2)[:str(real_of_sqrt2).find('.')])+1
            if '.99999999' in str(im_of_sqrt1):
                im_of_sqrt1 = int(str(im_of_sqrt1)[:str(im_of_sqrt1).find('.')])+1
            if '.99999999' in str(im_of_sqrt2):
                im_of_sqrt2 = int(str(im_of_sqrt2)[:str(im_of_sqrt2).find('.')])+1

            return f"{-1*((-im)**0.5)*sqrt_re_1:.{precision}f}+{sqrt_im_1*((-im)**0.5):.{precision}f}i", f"{-1*((-im)**0.5)*sqrt_re_2:.{precision}f}{sqrt_im_2*((-im)**0.5):.{precision}f}i"


    D = (-4 * re + 4 * ((re ** 2 + im ** 2) ** 0.5)) / 8

    sqrt_im_1 = D**0.5
    sqrt_im_2 = -D**0.5

    sqrt_re_1 = im/(2*sqrt_im_1)
    sqrt_re_2 = im/(2*sqrt_im_2)

    if all(x == '0' for x in str(sqrt_re_1)[str(sqrt_re_1).find('.') + 1:]):
        sqrt_re_1 = int(sqrt_re_1)

    if all(x == '0' for x in str(sqrt_re_2)[str(sqrt_re_2).find('.') + 1:]):
        sqrt_re_2 = int(sqrt_re_2)

    if all(x == '0' for x in str(sqrt_im_1)[str(sqrt_im_1).find('.') + 1:]):
        sqrt_im_1 = int(sqrt_im_1)

    if all(x == '0' for x in str(sqrt_im_2)[str(sqrt_im_2).find('.') + 1:]):
        sqrt_im_2 = int(sqrt_im_2)

    if '.00000000' in str(sqrt_im_1):
        sqrt_im_1 = int(str(sqrt_im_1)[:str(sqrt_im_1).find('.')])
    if '.00000000' in str(sqrt_im_2):
        sqrt_im_2 = int(str(sqrt_im_2)[:str(sqrt_im_2).find('.')])
    if '.00000000' in str(sqrt_re_1):
        sqrt_re_1 = int(str(sqrt_re_1)[:str(sqrt_re_1).find('.')])
    if '.00000000' in str(sqrt_re_2):
        sqrt_re_2 = int(str(sqrt_re_2)[:str(sqrt_re_2).find('.')])

    if '.99999999' in str(sqrt_im_1):
        sqrt_im_1 = int(str(sqrt_im_1)[:str(sqrt_im_1).find('.')]) + 1
    if '.99999999' in str(sqrt_im_2):
        sqrt_im_2 = int(str(sqrt_im_2)[:str(sqrt_im_2).find('.')]) + 1
    if '.99999999' in str(sqrt_re_1):
        sqrt_re_1 = int(str(sqrt_re_1)[:str(sqrt_re_1).find('.')]) + 1
    if '.99999999' in str(sqrt_re_2):
        sqrt_re_2 = int(str(sqrt_re_2)[:str(sqrt_re_2).find('.')]) + 1

    return f"{sqrt_re_1:.{precision}f}+{sqrt_im_1:.{precision}f}i",f"{sqrt_re_2:.{precision}f}{sqrt_im_2:.{precision}f}i"



app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/",response_class = HTMLResponse)
def get_main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "Результат"})

@app.post("/post_num")
def get_number(request: Request, number: str = Form(...), precision: str = Form()):
    if number.isdigit() and int(number)>0:
        if all(x=='0' for x in str((int(number))**0.5)[str((int(number))**0.5).find('.')+1:]):
            return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "", "number" : number, "result": f"{(int((int(number))**0.5)):.{precision}f} ; {(int(-(int(number)**0.5))):.{precision}f}"})
        else:
            return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "", "number" : number, "result": f"{((int(number))**0.5):.{precision}f} ; {(-(int(number)**0.5)):.{precision}f}"})
    if number.count(".")==1 and number.count('-')==0:
        buf = number.split(".")
        if buf[0].isdigit() and buf[1].isdigit():
            return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "", "number": number, "result": f"{((float(number))**0.5):.{precision}f} ; {(-(float(number))**0.5):.{precision}f}"})
    if number.isdigit() and int(number)==0:
        return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "Результат вычисления корня из нуля", "number": number, "result": f"{0:.{precision}f}"})
    if number[0]=='-' and number[1:].isdigit():
        result_1 = (-1*int(number))**0.5
        result_2 = -((-1*int(number))**0.5)
        buf_1 = str(result_1).split(".")
        if all(x == '0' for x in buf_1[1]):
            result_1 = int((-1*int(number))**0.5)
            result_2 = int(-((-1*int(number))**0.5))
        if (result_1==1) and (result_2==-1):
            return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "", "number": number, "result": f"i ; -i"})
        else:
            return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "", "number": number, "result": f"{result_1:.{precision}f}i ; {result_2:.{precision}f}i"})
    if number.count(".")==1 and number[0]=='-':
        buf_2 = number[1:].split(".")
        if buf_2[0].isdigit() and buf_2[1].isdigit():
            return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "", "number": number, "result": f"{((-1*float(number))**0.5):.{precision}f}i ; {(-((-1*float(number))**0.5)):.{precision}f}i"})
    if is_complex(number):
        a,b = get_re_and_im(number)
        result = get_complex_sqrt(a,b,precision)
        return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "", "number": number, "result": f"{result[0]} ; {result[1]}"})


    return templates.TemplateResponse("index.html", {"request": request, "type_of_result": "", "error":"something"})

# if __name__=="main":
#     uvicorn.run("main:app", host="0.0.0.0")