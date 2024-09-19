import qrcode # Pra criar o QrCode
from PIL import Image, ImageDraw, ImageFont # Pra renderizar e salvar a imagem
import os # Pra ler o arquivo de texto

def createImage(classeText, qrText, descText, savePath):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=3,
    )
    qr.add_data(qrText)
    qr.make(fit=True)
    qrCodeImage = qr.make_image(fill_color="black", back_color="white")
    qrCodeSize = qrCodeImage.size

    imageWidth = qrCodeSize[0]
    imageHeight = qrCodeSize[1] + 120
    image = Image.new('RGB', (imageWidth, imageHeight), color='white')
    draw = ImageDraw.Draw(image)
    
    qrCodeY = imageHeight - qrCodeSize[1]+10
    image.paste(qrCodeImage, (0, qrCodeY))
    
    classeFont = ImageFont.truetype("arialbd.ttf", 25)
    qrFont = ImageFont.truetype("arialbd.ttf", 17)
    descFont = ImageFont.truetype("arialbd.ttf", 15)

    classeTextBox = draw.textbbox((0, 0), classeText, font=classeFont)
    classeTextWidth = classeTextBox[2] - classeTextBox[0]
    classeTextX = (imageWidth - classeTextWidth) / 2
    classeTextY = 15
    draw.text((classeTextX, classeTextY), classeText, fill="black", font=classeFont)
    
    qrTextBox = draw.textbbox((0, 0), qrText, font=qrFont)
    qrTextWidth = qrTextBox[2] - qrTextBox[0]
    qrTextX = (imageWidth - qrTextWidth) / 2
    qrTextY = classeTextY + 35
    draw.text((qrTextX, qrTextY), qrText, fill="black", font=qrFont)

    def drawMultilineText(draw, text, position, font, maxWidth):
        lines = []
        words = text.split(' ')
        line = []
        for word in words:
            testLine = ' '.join(line + [word])
            testLineSize = draw.textbbox((0, 0), testLine, font=font)
            if testLineSize[2] <= maxWidth:
                line.append(word)
            else:
                lines.append(' '.join(line))
                line = [word]
        lines.append(' '.join(line))
        
        y = position[1]
        for line in lines:
            lineWidth = draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0]
            x = (maxWidth - lineWidth) / 2 + position[0]
            draw.text((x, y), line, font=font, fill="black")
            y += draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]+ 3.5
    
    descTextX = 10
    descTextY = qrTextY + 30
    drawMultilineText(draw, descText, (descTextX, descTextY), descFont, imageWidth - 20)

    image.save(savePath)

pasta = "qr_codes"

def remove_accents(text):
    accents = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c',
        'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A', 'Ä': 'A',
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
        'Ó': 'O', 'Ò': 'O', 'Õ': 'O', 'Ô': 'O', 'Ö': 'O',
        'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U',
        'Ç': 'C'
    }

    no_accent_text = ''.join(accents.get(char, char) for char in text)

    return no_accent_text

with open("lista.txt", "r", -1, "utf-8") as file:
    linhas = file.readlines()
    for linha in linhas:
        separacoes = linha.split("	")
        if len(separacoes) == 3:
          createImage(separacoes[1], separacoes[0], remove_accents(separacoes[2]), f"{pasta}/{separacoes[0]}.png")
          print(f"Criando imagem numero {separacoes[0]}")





