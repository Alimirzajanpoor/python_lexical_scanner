#نکته ی بسیار مهم: این برنامه به علت استفاده کردن از سویج-کیس نیاز به پایتون بالای نسخه ی 3.10 دارد
#اگر به نسخه ی 3.10 دسترسی ندارید  کافیست از این تابع زیریت را جایگزین تابع فعلی کنید
# def lookup(the_character):
#     if the_character == '+':
#         return 20
#     elif the_character == '-':
#         return 21
#     elif the_character == '*':
#         return 22
#     elif the_character == '/':
#         return 23
#     elif the_character == '(':
#         return 24
#     elif the_character == ')':
#         return 25
#     elif the_character == '=':
#         return 26
#     elif the_character == ':':
#         return 27
#     elif the_character == '"':
#         return 28
#     elif the_character == ',':
#         return 29
#     elif the_character == "\n":
#         return 30
#     elif the_character == "++":
#         return 31
#     elif the_character == "--":
#         return 32
#     else:
#         return -1
#.........................................................................................................................................
# اینجا یک توضیح سریع در مورد چگونگی عملکرد این کد قرار دارد:

# 1. شروع:
#    - `the_position` نشون‌دهنده مکان فعلی در متن ورودی است.
#    - داریم یک کلاس به نام `element` که برای نمایش هر توکن اطلاعات مربوطه‌اش رو داره.

# 2. جستجوی توکن:
#    - تابع `lookup` هر کاراکتر رو به کد توکن متناظرش تبدیل می‌کنه.

# 3. دسته‌بندی کاراکترها:
#    - تابع `getChar` کاراکترها رو به دسته‌های حروف، اعداد، نقطه اعشار و ... تقسیم می‌کنه.

# 4. تجزیه و تحلیل لغوی (`lex` function):
#    - تابع `lex` بر اساس نوع کاراکترها توکن‌ها رو از متن استخراج می‌کنه.
#    - حلقه اصلی برای هر کاراکتر از تابع‌های `getChar` و `lookup` استفاده می‌کنه.

# 5. گرفتن توکن بعدی:
#    - تابع `get_next_token` توکن بعدی رو برمی‌گردونه و موقعیت `the_position` رو به‌روز می‌کنه.
#    - تا زمانی که به انتهای متن (EOF) نرسیم، توکن‌ها رو گرفته و چاپ می‌کنیم.

# 6. اجرای کد:
#    - متن از یک فایل متنی خونده می‌شه.
#    - با فراخوانی `get_next_token`، توکن اولیه گرفته شده و چاپ می‌شه.
#    - سپس به ازای هر توکن بعدی، تا زمانی که به انتهای متن (EOF) نرسیم، توکن‌ها رو گرفته و چاپ می‌کنیم.
#.........................................................................................................................................
the_position = 0

class element:
    def __init__(self, token, lexeme, position):
        self.token = token  # نوع توکن
        self.lexeme = lexeme  # متن متناظر با توکن
        self.position = position  # موقعیت (ایندکس) توکن در متن

def lookup(the_character):
    # تابعی برای یافتن توکن متناظر با یک کاراکتر
    match the_character:
        case '+':
            return 20
        case '-':
            return 21
        case '*':
            return 22
        case '/':
            return 23
        case '(':
            return 24
        case ')':
            return 25
        case '=':
            return 26
        case ':':
            return 27
        case '"':
            return 28
        case ',':
            return 29
        case "\n":
            return 30
        case "++":
            return 31
        case "--":
            return 32
        case _:
            return -1

def getChar(nextChar):
    # تابعی برای تشخیص نوع کاراکتر (حرف، عدد، نقطه و غیره)
    if 'a' <= nextChar <= 'z' or 'A' <= nextChar <= 'Z':
        return 'LETTER'
    elif nextChar == '.':
        return 'DECIMAL_POINT'
    elif '0' <= nextChar <= '9':
        return 'DIGIT'
    elif nextChar == ' ':
        return 'SPACE'
    else:
        return 'UNKNOWN'

def lex(nextString):
    # تابع اصلی برای تولید توکن‌ها از رشته ورودی
    global the_position
    while the_position < len(nextString):
        identity = getChar(nextString[the_position])

        if identity == 'LETTER':
            temp = ''
            # حلقه برای جمع‌آوری حروف تا وقتی که به فاصله یا کاراکتر ناشناخته برخورد شود
            while(the_position < len(nextString) and getChar(nextString[the_position]) != 'SPACE' and getChar(nextString[the_position]) != 'UNKNOWN'):
                if getChar(nextString[the_position]) == 'LETTER' or getChar(nextString[the_position]) == 'DIGIT':
                    temp += nextString[the_position]
                the_position += 1
            e1 = element('IDENT', temp, the_position)
            return e1

        elif identity == 'DIGIT':
            decimal_found = False
            temp = ''
            # حلقه برای جمع‌آوری ارقام و شناسایی اعشار
            while(the_position < len(nextString) and getChar(nextString[the_position]) != 'SPACE' and getChar(nextString[the_position]) != 'UNKNOWN'):
                char_identity = getChar(nextString[the_position])
                if char_identity == 'DIGIT':
                    temp += nextString[the_position]
                elif char_identity == 'DECIMAL_POINT' and not decimal_found:
                    temp += nextString[the_position]
                    decimal_found = True
                else:
                    break
                the_position += 1
            # تشخیص اینکه آیا اعشاری یا صحیح است
            if decimal_found:
                e1 = element('FLOAT_LIT', temp, the_position)
            else:
                e1 = element('INT_LIT', temp, the_position)
            return e1

        elif identity == 'UNKNOWN':
            nextToken = lookup(nextString[the_position])
            temp_position = the_position + 1
            e1 = element(str(nextToken), nextString[the_position], temp_position)
            return e1

        the_position += 1

def get_next_token(the_text, move_position):
    # تابع برای گرفتن توکن بعدی از رشته
    global the_position
    if len(the_text) != the_position:
        if move_position == False:
            temp = the_position
            result = lex(the_text)
            the_position = temp
            return result
        result = lex(the_text)
        the_position = result.position
        return result
    else:
        result = element('EOF', 'EOF', the_position)
        return result

# خواندن متن از یک فایل متنی
file_name=input("input file name with(.txt): ")
the_file = open(file_name)
the_text = the_file.read()

# گرفتن توکن ابتدایی
result = get_next_token(the_text, True)
counter = 1
print("Next token: " + result.token + " | Next Lexeme: " + result.lexeme + " | line :" + str(counter))

# گرفتن و چاپ توکن‌ها تا رسیدن به پایان فایل (EOF)
while result.token != 'EOF':
    result = get_next_token(the_text, True)
    if result.lexeme != "\n":
        print("Next token: " + result.token + " | Next Lexeme: " + result.lexeme + " | line :" + str(counter))
    else:
        counter = counter + 1
