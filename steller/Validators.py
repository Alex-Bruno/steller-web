def numbersValid(text):
    number = text.strip()
    return ''.join([i for i in number if i.isdigit()])


def charsValid(text):
    chars = text.strip()
    return ''.join([i for i in chars if not i.isdigit()])


def validatePlate(text):
    text = text.strip()
    text.replace(' ', '')
    if len(text) == 7:
        chars = text[0:3]
        number = text[3:7]
    elif len(text) == 8:
        chars = text[0:3]
        number = text[4:8]
    else:
        return None

    if chars and number:
        number = numbersValid(number)
        chars = charsValid(chars)

        if len(chars) == 3 and len(number) == 4:
            string = chars + '-' + str(number)
            return string

    return None
