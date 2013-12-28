import numpy as np
import cv2, os, sys
import itertools
import pygame
from pygame.rect import Rect
import math
import collections
from collections import OrderedDict
import easygui as eg

filterParams=OrderedDict([
    ['Points Count',[0,100000]],
    ['Rect Proportion',[0.1,10]],
    ['AreaSquare Koef',[0.1,1]],
    ['Area',[0.001,0.9]],
    ['Width',[0.01,1]],
    ['Heigh',[0.01,1]],
    ['X',[0,1]],
    ['Y',[0,1]],
    ['Out resolution px',[198,148]],
    ])

def sqFilter(iw,ih,r,area,cnt):
    """
      square filter func
    """
    lCnt=len(cnt)

    koef=r.w*1.0/r.h
    areaKoef=area*1.0/(r.w*r.h)

    def check(v,param):
        arr=filterSettings[param]
        if v>=arr[0] and v<=arr[1]:
            return 1
        if param=='X':
            print v
        return 0

    return check(lCnt,'Points Count') and check(koef,'Rect Proportion') and check(areaKoef,'AreaSquare Koef') and check(area*1.0/(iw*ih),'Area') and check(r.w*1.0/iw,'Width') and check(r.h*1.0/ih,'Heigh') and r.collidelist(excludeSquares) and check(r.x*1.0/iw,'X') and check(r.y*1.0/ih,'Y')


def find_squares(img):
    """
      search for squares
    """
    iw,ih=imgClone.shape[1],imgClone.shape[0]
    imgSq=iw*ih#img.shape[0]*img.shape[1]

    lineH=2
    cv2.line(img,(0,ih-lineH),(iw-lineH,ih-lineH),lineH)
    cv2.line(img,(iw-lineH,0),(iw-lineH,ih-lineH),lineH)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)

    squares = []
    sortedSquares={}
    for gray in cv2.split(gray):
        if 1==1:
            bin = cv2.adaptiveThreshold(gray,255, cv2.ADAPTIVE_THRESH_MEAN_C,1,15,4)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt=cv2.convexHull(cnt)#[[x,y],[x+w,y],[x+w,y+h],[x,y+h]]
                area=cv2.contourArea(cnt)
                x,y,w,h = cv2.boundingRect(cnt)
                r=Rect(x,y,w,h)
                if sqFilter(iw,ih,r,area,cnt):
                    k=(w-w%10,h-h%10)
                    lst=sortedSquares.setdefault(k,[])
                    lst.append(cnt)

    vv=sortedSquares.values()
    vv=list(itertools.chain(*vv))
    vv1=map(cv2.boundingRect,vv)
    vv1=map(Rect,vv1)

    i=0
    while i<len(vv1):
        flTest=vv1[i].collidelist(vv1[i+1:])
        if flTest>=0:
            r1,r2=vv1[i],vv1[i+1+flTest]
            # if rect size >
            pInd=i
            if (r1.w*r1.h)>(r2.w*r2.h):
                pInd=i+1+flTest
#                i+=1
            vv.pop(pInd)
            vv1.pop(pInd)
        else:
            i+=1

    # fix lines
##    minW=w*0.8
##    minH=h*0.8
##    maxDelta=3
##    for o in vv:
##        x,y,w,h = cv2.boundingRect(o)
##        for i in xrange(len(o)):
##            p1,p2=o[i-1][0],o[i][0]
##            #dist=math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
##            if abs(p1[0]-p2[0])>minW and abs(p1[1]-p2[1])<maxDelta:
##
##                p2[1]=
##            elif abs(p1[1]-p2[1])>minH and abs(p1[0]-p2[0])<maxDelta:
##                print p1,p2
    lCut=cutLines
# cut 2 lines from all sides
    if cutLines:
        for o in vv:
            x,y,w,h = cv2.boundingRect(o)
            x,y=x+lCut,y+lCut
            x1,y1=x+w-lCut*2,y+h-lCut*2
            for i in xrange(len(o)):
                p=o[i][0]
                #dist=math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
                if p[0]<x:
                    p[0]=x
                if p[0]>x1:
                    p[0]=x1
                if p[1]<y:
                    p[1]=y
                if p[1]>y1:
                    p[1]=y1

    return vv
    return squares

#from win32api import GetSystemMetrics
#print "width =", GetSystemMetrics (0)
#print "height =",GetSystemMetrics (1)
#exit(0)

#    1 millimeter [mm] = 3.77952755905511 pixel (Y)
def ToSvg(img,squares):
    import simplesvg
    reload(simplesvg)

    iw,ih=imgClone.shape[1],imgClone.shape[0]
##    inf=eg.Tk()
##    inf.winfo_x=-100
##    #1010 px, 660
##    sw_mm,sh_mm=inf.winfo_screenmmwidth(),inf.winfo_screenmmheight()
##    sw_px,sh_px=inf.winfo_screenwidth(),inf.winfo_screenheight()
##    filterSettings.update(GetSteps()[0])
    wMm,hMm=map(float,filterSettings['Out resolution px'])
##    wPx,hPx=(sw_px*wMm*1.0/sw_mm),(sh_px*hMm*1.0/sh_mm)
##    xKoef,yKoef=wPx*1.0/iw,hPx*1.0/ih
    xKoef,yKoef=wMm*1.0/iw,hMm*1.0/ih
    # group by top
#    iw,ih=img.shape[1],img.shape[0]
    svg=simplesvg.SVG(iw*xKoef,ih*yKoef)
    print 'squares=',len(squares)
#    def Transfrom(pt,koef):
#        pass

    for k, v in itertools.groupby(squares,lambda x : cv2.boundingRect(x)[1]):
        objs=list(v)
        svgObjs=[]
        for sq in objs:
            p=simplesvg.Polygon([[x[0][0]*xKoef,x[0][1]*yKoef] for x in sq],style="fill:none;stroke:#010101;stroke-width:0.0283;")
            svgObjs.append(p)
        svg.group(svgObjs)

    rSvg=svg.to_xml()
    print 'rSvg=',len(rSvg)
    oname=fname.lower().replace('.png','.svg')
    if oname==fname:
        raise BaseException('error')
    with open(oname,'wb') as f:
        f.write(rSvg)
    return rSvg

filterSettings=filterParams
filterSettingsDef=OrderedDict(zip(filterSettings.keys(),[[0,100000],[0.2,2],[0.7,1],[0.001,0.9],[0.02,0.5],[0.02,0.5]]))

fltParams={}
if os.path.exists('params.ini'):
    with open('params.ini','r') as f:
        sets=f.read()
        if sets:
            fltParams=eval(sets)

def SetSteps(steps=[]):
    try:
        while tSteps.size():
            tSteps.delete(0)
        ind=0
        for x in steps:
            tSteps.insert(ind,x)
            ind+=1
    except:
        pass

def GetSteps():
    try:
        return map(eval,map(tSteps.get,xrange(tSteps.size())))
    except:
        return fltParams[fname]
        pass

def SaveAllSteps(curSteps=[]):
    if len(curSteps):
        SetSteps(curSteps)
    fltParams[fname]=list(map(lambda x : (isinstance(x,basestring) and eval(x)) or x,curSteps))
    with open('params.ini','w') as f:
        f.write(str(fltParams))

def onAddStep(evt):
    SaveAllSteps(GetSteps()+[CurSettings()])

def split_seq(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))

def CurSettings():
    vals=list(split_seq([float(entryWidget.get()) for entryWidget in eg.entryWidgets],2))
    return OrderedDict(zip(filterSettings.keys(),vals))

def Refresh(stepLst):
    global excludeSquares,img
    SaveAllSteps(GetSteps())
    img=imgClone.copy() #cv2.cv.CloneImage(imgClone)
    squares=[]
    excludeSquares=[]
    for step in stepLst:
#    vals=CurSettings()
        filterSettings.update(step)
        sqs=find_squares(img)
        excludeSquares+=[Rect(cv2.boundingRect(sq)) for sq in sqs]
        squares += sqs

    if flGuiMode:
        cv2.drawContours(img, squares, -1, (0, 255, 0), 3)
        img=cv2.resize(img,(img.shape[1]/3,img.shape[0]/3))
        cv2.imshow('squares', img)
    return squares

def onRefresh(evt):
    filterSettings.update(CurSettings())
    Refresh([filterSettings])

def onRefreshAll(evt):
    sqs=Refresh(steps)
    print len(sqs)
    ToSvg(imgClone,sqs)

def findSimilar(fn):
    lst=[fltParams[x] for x in fltParams.keys() if x.startswith(fn[:5])]
    if not lst:
        lst=[filterSettingsDef]
    return lst[0]

excludeSquares=[]

def onStepsKey(evt):
    if evt.keycode==46:
        map(tSteps.delete,sorted(map(int,tSteps.curselection()),reverse=True))

def CustomControls(funcFrom,boxRoot,buttonsFrame):
    global tSteps
    tSteps=eg.Listbox(boxRoot,height=3, borderwidth="1m", relief="flat", bg="white")
    tSteps.bind("<Key>", onStepsKey)
    tSteps.configure(font=(eg.PROPORTIONAL_FONT_FAMILY,eg.PROPORTIONAL_FONT_SIZE))
    tSteps.pack(side=eg.LEFT, fill=eg.BOTH, expand=eg.YES)

    confButton = eg.Button(buttonsFrame, takefocus=eg.NO, text="Add to steps", height=1, width=13)
    confButton.pack(expand=eg.YES, side=eg.LEFT)
    confButton.bind("<Button-1>", onAddStep)

    refreshButton = eg.Button(buttonsFrame, takefocus=eg.NO, text="Refresh", height=1, width=13)
    refreshButton.pack(expand=eg.YES, side=eg.LEFT)
    refreshButton.bind("<Button-1>", onRefresh)

    refreshAllButton = eg.Button(buttonsFrame, takefocus=eg.NO, text="Refresh All", height=1, width=13)
    refreshAllButton.pack(expand=eg.YES, side=eg.LEFT)
    refreshAllButton.bind("<Button-1>", onRefreshAll)

    SetSteps(map(str,steps))
    onRefreshAll(None)

eg.onCustomControl=CustomControls

def ProcessImage(fn):
    global img,imgClone,fname,steps
    fname=fn
    img = cv2.imread(fn)
    imgClone=img.copy()#cv2.cv.CloneImage(img)
    steps=fltParams.get(fn, None)
    if not steps:
        steps=findSimilar(fn)

    filterSettings.update(steps[0])

    fields=[]
    vals=[]
    for k,v in filterSettings.items():
        if k=='Out resolution px':
            fields+=[k+' width',k+' height']
        else:
            fields+=[k+' Min',k+' Max']
        vals+=v
    if flGuiMode:
        ret=eg.multenterbox(fields=fields,values=vals)
    onRefreshAll(None)


flGuiMode=(len(sys.argv)>1 and (sys.argv[1]=='setup')) or 0
cutLines=int((len(sys.argv)>2 and sys.argv[2]) or 2)
steps=[]
print 'GuiMode=',flGuiMode,'cutLines=',cutLines
if __name__ == '__main__':
    from glob import glob
    for fn in glob('samples/*.png'):
	print 'ProcessImage',fn
        ProcessImage(fn)
    cv2.destroyAllWindows()
