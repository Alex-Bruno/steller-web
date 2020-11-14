from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from datetime import datetime
import traceback
#
import imagezmq
import cv2
import numpy as np
#
# python standard lib
import base64
#
from accessApp.models import Access, Vehicle


@api_view(['POST'])
@permission_classes((AllowAny,))
def api_save_access(request):
    try:
        plate = request.data['plate']
        if (validatePlate(plate) == None):
            raise Exception("Placa indefinida")
    except:
        return Response({'Erro': 'Placa indefinida'}, status=HTTP_404_NOT_FOUND)

    try:
        vehicle = Vehicle.objects.filter(plate=plate).first()

        access = Access.objects.filter(
            plate=plate, exit__isnull=True).first()

        if access:
            access.exit = datetime.now()
            access.save()
        else:
            if vehicle:
                access = Access(
                    vehicle=vehicle,
                    plate=plate,
                    entrance=datetime.now()
                )
            else:
                access = Access(
                    plate=plate,
                    entrance=datetime.now()
                )
            access.save()

        return Response({'success': True, 'acess': access.plate})
    except:
        return Response({'error': 'Falha ao tentar salvar o acesso'}, status=HTTP_400_BAD_REQUEST)


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

def numbersValid(text):
    number = text.strip()
    return ''.join([i for i in number if i.isdigit()])

def charsValid(text):
    chars = text.strip()
    return ''.join([i for i in chars if not i.isdigit()])

@api_view(['POST'])
@permission_classes((AllowAny,))
def api_receive_image(request):
    try:
        print('imagem recebida')
        base64_img = request.data['image']
    except:
        return Response({'Erro': 'Imagem indefinida'}, status=HTTP_404_NOT_FOUND)

    try:
        # ip = args["ip"]
        ip = '192.168.2.106'

        sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(ip))

        img = readb64(base64_img)
        sender.send_image('web', img)

        return Response({'success': True, 'images': base64_img})
    except Exception as e:
        #return Response({'error': 'Falha ao tentar enviar a imagem'}, status=HTTP_400_BAD_REQUEST)
        print(traceback.format_exc())
        return Response({'error': True}, status=HTTP_400_BAD_REQUEST)


def readb64(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img