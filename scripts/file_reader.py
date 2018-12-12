import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go
import plotly
import tempfile as t
import os
import base64
import io
import tempfile
from decimal import Decimal

videoTime = list();
neutral = list();
happy = list();
sad = list();
angry = list();
surprised = list();
scared = list();
disgusted = list();
countlist = list();
Global_Checker = bool()

Stimulus = list();
EventMarker = list();


def clean_all():
    videoTime.clear();
    neutral.clear();
    happy.clear()
    sad.clear()
    angry.clear()
    surprised.clear()
    scared.clear()
    disgusted.clear()
    countlist.clear()

    Stimulus.clear()
    EventMarker.clear()


def read_file(contents):
    clean_all()

    f = tempfile.TemporaryFile(mode="w+b")

    data = base64.b64decode(contents)

    dados = data.decode('utf-8')
    f.write(bytes(dados, 'utf-8'))
    f.seek(0)
    for i in range(0, 10):
        linha = f.readline().decode()

    while linha:
        if linha.__len__() > 8:
            word = linha.split('\t')
            videoTime.append(word.__getitem__(0))
            neutral.append(word.__getitem__(1))
            happy.append(word.__getitem__(2))
            sad.append(word.__getitem__(3))
            angry.append(word.__getitem__(4))
            surprised.append(word.__getitem__(5))
            scared.append(word.__getitem__(6))
            disgusted.append(word.__getitem__(7))
            Stimulus.append(word.__getitem__(8))
            EventMarker.append(word.__getitem__(9))
        linha = f.readline().decode()
    clean_time()
    failsCheck(neutral, happy, sad, angry, surprised, scared, disgusted)
    buildCountList(neutral)
    # change_time_format()
    f.close()


def make_pie_data():
    tneutral = [Decimal(x.strip(' "')) for x in neutral]
    thappy = [Decimal(x.strip(' "')) for x in happy]
    tsad = [Decimal(x.strip(' "')) for x in sad]
    tangry = [Decimal(x.strip(' "')) for x in angry]
    tsurprised = [Decimal(x.strip(' "')) for x in surprised]
    tscared = [Decimal(x.strip(' "')) for x in scared]
    tdisgusted = [Decimal(x.strip(' "')) for x in disgusted]

    dsgstd = 0
    scrd = 0
    sprsd = 0
    angr = 0
    sd = 0
    hpp = 0
    ntrl = 0

    for i in range(len(neutral)):
        b = [tneutral[i], thappy[i], tsad[i], tangry[i], tsurprised[i], tscared[i], tdisgusted[i]]
        maximo = max(b)
        c = b.index(maximo)
        if c == 0: ntrl += 1
        if c == 1: hpp += 1
        if c == 2: sd += 1
        if c == 3: angr += 1
        if c == 4: sprsd += 1
        if c == 5: scrd += 1
        if c == 6: dsgstd += 1
    print(ntrl, " ", hpp, " ", sd, " ", angr, " ", sprsd, " ", scrd, " ", dsgstd, " ")
    data = [ntrl, hpp, sd, angr, sprsd, scrd, dsgstd]

    return data


def clean_time():
    for i in range(len(neutral)):
        if neutral.__getitem__(i).__eq__("FIND_FAILED") or neutral.__getitem__(i).__eq__("FIT_FAILED"):
            videoTime[i] = "missing data"

    while 'Missing data' in videoTime: videoTime.remove('Missing data')


def change_time_format():
    for item in videoTime:
        hr,min,seg = item.split(':')

        if hr == "00" and min == '00':
            videoTime[videoTime.index(item)] = seg
        if hr == "00" and min != '00':
            videoTime[videoTime.index(item)] = min+":"+seg

    print(videoTime)

def buildCountList(lista):
    for i in range(len(lista)):
        countlist.append(i)


def failsCheck(*args):
    for elem in args:
        checklist = elem
        while 'FIND_FAILED' in checklist: checklist.remove('FIND_FAILED')
        while 'FIT_FAILED' in checklist: checklist.remove('FIT_FAILED')


def create_data_figure(x_list):

    trace0 = go.Scatter(
        x=x_list,
        y=neutral,
        mode='lines',
        name='neutral',
        hoverinfo='neutral',
        # connectgaps=True,


    )

    trace1 = go.Scatter(
        x=x_list,
        y=happy,
        mode='lines',
        name='happy',
        hoverinfo='happy',
        # connectgaps=True

    )

    trace2 = go.Scatter(
        x=x_list,
        y=sad,
        mode='lines',
        name='sad',
        hoverinfo='sad',
        # connectgaps=True

    )

    trace3 = go.Scatter(
        x=x_list,
        y=angry,
        mode='lines',
        name='angry',
        hoverinfo='happy',
        # connectgaps=True

    )

    trace4 = go.Scatter(
        x=x_list,
        y=surprised,
        mode='lines',
        name='surprised',
        hoverinfo='surprised',
        # connectgaps=True

    )

    trace5 = go.Scatter(
        x=x_list,
        y=scared,
        mode='lines',
        name='scared',
        hoverinfo='scared',
        # connectgaps=True

    )

    trace6 = go.Scatter(
        x=x_list,
        y=disgusted,
        mode='lines',
        name='disgusted',
        hoverinfo='disgusted',
        # connectgaps=True


    )

    data = [trace0, trace1, trace2, trace3, trace4, trace5, trace6]

    return data
