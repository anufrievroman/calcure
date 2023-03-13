def strike_0(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

def strike_1(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])

def strike_2(text):
    return '\u0336' + '\u0336'.join(text) + '\u0336'

print(strike_2("My text"))
