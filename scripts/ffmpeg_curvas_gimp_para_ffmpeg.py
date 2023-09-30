#!/usr/bin/python

# Adaptado por mpt.
# Fonte: https://github.com/NapoleonWils0n/cerberus/blob/master/ffmpeg/ffmpeg-white-balance.org.

import sys
import re
import pyperclip

#make generator
lower=0
upper=1
length=256
zerotoonestepped256gen = [lower + x*(upper-lower)/length for x in range(length)]

def formatForFFMPEG(values):
    serializedValues = values.split(' ')
    list = []
    for i in range (len(serializedValues)):
        if not list or zerotoonestepped256gen[i] - float(re.match(r"^[^////]*",list[-1]).group(0)) > 0.01:
            list.append('%s/%s' % (zerotoonestepped256gen[i], serializedValues[i]))
    return list

#print instructions

if len(sys.argv) < 3:
    print('\nVersão 0.0.0', end = '\n\n')
    print('This is a tool to convert a color curves map from GIMP to a curves filter that can be inserted into the -complex_filter. Note that you still need to append the input and output streams onto either side of the command.', end = '\n\n')
    print('Uso:', end = '\n')
    print('ffmpeg_curvas_gimp_para_ffmpeg.py <entrada> <saida>', end = '\n\n')
    print('Para gerar o arquivo de entrada, dentro do Gimp, em qualquer ferramenta que manipule curvas (por exemplo, "Níveis" ou "Curvas"), basta exportar as definições da curva para um arquivo (clicar no botão com uma seta à esquerda no canto direito superior da caixa de diálogo para acessar a exportação).', end = '\n\n')
    print('Depois, para usar no FFmpeg, deve-se abrir o arquivo de saída e copiar a "grande" linha logo no início do arquivo, identificada com o rótulo "Final command" logo acima dela. Esta linha copiada deverá ser passada ao parâmetro -vf do FFmpeg.', end = '\n\n')
    print('Para maior facilidade, ao concluir, este "script" já deixa o comando final copiado na área de transferência ("clipboard").', end = '\n\n')
    print('Adaptado por "mpt" de https://github.com/NapoleonWils0n/cerberus/blob/master/ffmpeg/ffmpeg-white-balance.org.', end = '\n')
    sys.exit()


#get filename

file = sys.argv[1]
out = sys.argv[2]

#file = input('Please input the absolute path to the GIMP Color Curve Preset File: ')
#out = input('Please enter the output file (file will be overwritten if it exists): ')

#Open the curves file
curvesfile = open(file,"r")
curvesString = curvesfile.read()
foundValues = re.findall(r'(?<=samples 256) [\d. ]*',curvesString)

masterValues = formatForFFMPEG(foundValues[0][1:])
redValues = formatForFFMPEG(foundValues[1][1:])
greenValues = formatForFFMPEG(foundValues[2][1:])
blueValues = formatForFFMPEG(foundValues[3][1:])
alphaValues = formatForFFMPEG(foundValues[4][1:])

commandPrelim = 'curves=master="'

command = commandPrelim + ' '.join(masterValues) + '":red="' + ' '.join(redValues) +'":green="' + ' '.join(greenValues) + '":blue="' + ' '.join(blueValues) + '"'

pyperclip.copy(command)

with open(out, 'w') as out:
    out.write("Final Command\n\n" + command + '\n\n')
    out.write("master\n\n" + ' '.join(masterValues) + '\n\n')
    out.write("red\n\n" + ' '.join(redValues) + '\n\n')
    out.write("green\n\n" + ' '.join(greenValues) + '\n\n')
    out.write("blue\n\n" + ' '.join(blueValues) + '\n\n')
    out.write("alpha\n\n" + ' '.join(alphaValues) + '\n\n')
