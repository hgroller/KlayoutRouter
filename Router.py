# Enter your Python code here
#Python Proof of Concept for A* Routing
#Tracy Groller 3/19/21
#Below Code find's all Text and Routes Point to Point
#ToDo: Vertical and Horizontal metals
#          Drop vias at intersection
#          Add Maze array definition based on the Border Layer
#    
import pya
import numpy as np
import array
import sys
import math
import itertools
from importlib import reload
from collections import OrderedDict, Counter
import itertools

class OrderedCounter(Counter, OrderedDict): 
    pass
    
#Edit this too reflect you install path for Klayout
sys.path.append("C:/Users/Tracy/KLayout/pymacros")
import AstarRouter

#Reload main if changed in AstarRouter
reload(AstarRouter)
from AstarRouter import main

layout = pya.Application.instance().main_window().current_view().active_cellview().layout() 

if layout == None:
  raise Exception("No layout")

cv = pya.Application.instance().main_window().current_view().active_cellview()
dbu =layout.dbu

cell = pya.Application.instance().main_window().current_view().active_cellview().cell
if cell == None:
  raise Exception("No cell")

#Get the  Box Border
def GetBox():
  texts = 0
  layer_info = LayerInfo.new(13,0)
  layer = layout.layer(layer_info) 
  iter = layout.begin_shapes(cv.cell_index, layer)
  if iter.shape().is_box():
    ux =  iter.shape().box.right
    uy =  iter.shape().box.top
  return ux,uy  

def Get_Text():
  #Get the Text
  texts = 0
  layer_info = LayerInfo.new(9,0)
  layer = layout.layer(layer_info) 
  iter = layout.begin_shapes(cv.cell_index, layer)
  coords = []
  strlst = []
  while not iter.at_end():
    if iter.shape().is_text():
      string =  iter.shape().text.string
      x = iter.shape().text.x
      y = iter.shape().text.y
      strlst.append(string)
      lst = [string,x,y]
      coords.append(lst)
    iter.next()

  srt = sorted(coords)
 #Remove Duplicates from text list
  strlst = sorted(list(dict.fromkeys(strlst)))
  return strlst,srt

def coords(path):
    result = []
    for p in path:
      result.append(DPoint.new(p[0]/dbu,p[1]/dbu))
    return result

def create_path(crd,wd,lay):
  wdt = wd
  layer_info = LayerInfo.new(lay,0)
  layer_index = layout.layer(layer_info)
  cv.cell.shapes(layer_index).insert(Path.new(crd,wd/dbu))   

def create_box(crd,lay):
  layer_info = LayerInfo.new(lay,0)
  layer_index = layout.layer(layer_info)
  cv.cell.shapes(layer_index).insert(Box.new(crd[0],crd[1]))

#Filter the list to Search the text list
#For A* Routing 
#This works for 2 pins only at the present time
#ie: Pin A/Pin A.
#Placements of text can be anywhere

def Router():

  stlst,srt = Get_Text()
  filtered = None
  for search in stlst: 
    filtered = list(filter(lambda x:x[0]==search,srt))
 
    wd = .3
    lay = 11
    #Testing
     
    l1  = filtered[0][1]/1000
    l2  = filtered[0][2]/1000
    
    l3  = filtered[1][1]/1000
    l4  = filtered[1][2]/1000
    
    #Get Decimal from float
    x1a = l1 - int(l1)
    y1a = l2 - int(l2)
    x2a = l3 - int(l3)
    y2a = l4 - int(l4)
   
    lc1  = int(filtered[0][1]/1000)
    lc2  = int(filtered[0][2]/1000)
    lc3  = int(filtered[1][1]/1000)
    lc4  = int(filtered[1][2]/1000)
   
    loc1 = (lc1,lc2)
    loc2 = (lc3,lc4)
    



    
    pth  = AstarRouter.main(loc1,loc2)

    
  #Parse in the Vert/Horz Coords
    vert = [el[0] for el in pth]
    horz = [el[1] for el in pth]

    hoz = [k for k, v in OrderedCounter(horz).items() if v > 1]
    vet = [k for k, v in OrderedCounter(vert).items() if v > 1]

   
    #Build the Route Point to Point
    cnt =1
    lay = 9
    wd = .3
    hlen = len(hoz)
    for p in hoz:
      filteredh = list(filter(lambda x:x[1]==p,pth))
      if cnt != hlen:
       
        M = [x1a,y1a]
        hout = [[i+j for i,j in zip(subl, subm)] for subl, subm in zip(filteredh, itertools.cycle([M]))]
        crd = coords(hout)
        create_path(crd,wd,lay)
        cnt = cnt + 1
      else:
         M = [x1a,y1a]
         hout = [[i+j for i,j in zip(subl, subm)] for subl, subm in zip(filteredh, itertools.cycle([M]))]
         xx = x2a - x1a
         xxx = hout[1][0] + xx
         hout[1][0] = xxx
         yy = y2a - y1a
         yyy = hout[1][1] + yy
         hout[0][1] = yyy
         hout[1][1] = yyy
         crd = coords(hout)
         create_path(crd,wd,lay)
        
  
    cnt = 1
    wd = .3
    vlen = len(vet)
    

    for p in vet: 
      filteredv = list(filter(lambda x:x[0]==p,pth))
      if cnt != vlen:
       
          M = [x1a,y1a]
          vout = [[i+j for i,j in zip(subl, subm)] for subl, subm in zip(filteredv, itertools.cycle([M]))]
          crd = coords(vout)
          lay = 11
          create_path(crd,wd,lay)
          cnt = cnt + 1
          
     #Build Metal1/2 Overlap
          mwd =  wd / 2
          vwd = wd / 4
          x1 =  abs(int(crd[0].x)/1000)
          y1 =  abs(int(crd[0].y)/1000)
          x2 =  abs(int(crd[1].x)/1000)
          y2 =  abs(int(crd[1].y)/1000)
     #Metals
          lx1 = x1 - mwd
          ly1 = y1 - mwd
          ux1 = x1 + mwd
          uy1 = y1 + mwd
    
          lx2 = x2 - mwd
          ly2 = y2 - mwd
          ux2 = x2 + mwd
          uy2 = y2 + mwd
     
      #Via
          vx1 = x1 - vwd
          vy1 = y1 - vwd
          vux1 = x1 + vwd
          vuy1 = y1 + vwd
    
          vx2 = x2 - vwd
          vy2 = y2 - vwd
          vux2 = x2 + vwd
          vuy2 = y2 + vwd
     
     #Metals1/2
          path1 = [(lx1,ly1),(ux1,uy1)]
       #M = [x1a,y1a]
      #out = [[i+j for i,j in zip(subl, subm)] for subl, subm in zip(path1, itertools.cycle([M]))]
          crd1 = coords(path1)
          lay = 9
          create_box(crd1,lay)
          lay = 11
          create_box(crd1,lay)
     #Via
          via1 = [(vx1,vy1),(vux1,vuy1)]
          vcrd1 = coords(via1)
          lay = 10
          create_box(vcrd1,lay)
     
     #Metals1/2
          path2 = [(lx2,ly2),(ux2,uy2)]
          crd2 = coords(path2)
          lay = 9
          create_box(crd2,lay)
          lay = 11
          create_box(crd2,lay)
     
     #Via
          via2 = [(vx2,vy2),(vux2,vuy2)]
          vcrd2 = coords(via2)
          lay = 10
          create_box(vcrd2,lay)
      else:
          M = [x1a,y1a]
          vout = [[i+j for i,j in zip(subl, subm)] for subl, subm in zip(filteredv, itertools.cycle([M]))]
          vlen =  len(vout)
          xx = y2a - y1a
          xxx = vout[1][1] + xx
          vout[1][1] = xxx
          crd = coords(vout)
          lay = 11
          create_path(crd,wd,lay)
     #Build Metal1/2 Overlap
          mwd =  wd / 2
          vwd = wd / 4
          x1 =  abs(int(crd[0].x)/1000)
          y1 =  abs(int(crd[0].y)/1000)
          x2 =  abs(int(crd[1].x)/1000)
          y2 =  abs(int(crd[1].y)/1000)
     #Metals
          lx1 = x1 - mwd
          ly1 = y1 - mwd
          ux1 = x1 + mwd
          uy1 = y1 + mwd
    
          lx2 = x2 - mwd
          ly2 = y2 - mwd
          ux2 = x2 + mwd
          uy2 = y2 + mwd
     
      #Via
          vx1 = x1 - vwd
          vy1 = y1 - vwd
          vux1 = x1 + vwd
          vuy1 = y1 + vwd
    
          vx2 = x2 - vwd
          vy2 = y2 - vwd
          vux2 = x2 + vwd
          vuy2 = y2 + vwd
     
     #Metals1/2
          path1 = [(lx1,ly1),(ux1,uy1)]
       #M = [x1a,y1a]
      #out = [[i+j for i,j in zip(subl, subm)] for subl, subm in zip(path1, itertools.cycle([M]))]
          crd1 = coords(path1)
          lay = 9
          create_box(crd1,lay)
          lay = 11
          create_box(crd1,lay)
     #Via
          via1 = [(vx1,vy1),(vux1,vuy1)]
          vcrd1 = coords(via1)
          lay = 10
          create_box(vcrd1,lay)
     
     #Metals1/2
          path2 = [(lx2,ly2),(ux2,uy2)]
          crd2 = coords(path2)
          lay = 9
          create_box(crd2,lay)
          lay = 11
          create_box(crd2,lay)
     
     #Via
          via2 = [(vx2,vy2),(vux2,vuy2)]
          vcrd2 = coords(via2)
          lay = 10
          create_box(vcrd2,lay)
      
      
      
action1 = pya.Action()
action1.title = "Router"
action1.tool_tip = "Router"
action1.on_triggered(Router)
menu = pya.MainWindow.instance().menu()
# Insert it main menu: where, name, action:
#menu.insert_item("tools_menu.end", "Router", action1)
# Insert into toolbar: for the router
menu.insert_item("@toolbar.end", "Router", action1)


#Build Matrix for later
#Build Maze based on  Border Boundary Box
#rows = int(input()) ux from Border Box
#cols = int(input())  uy from Border Box

#rows = round(abs(int(ux))/1000)
#cols =  round(abs(int(uy))/1000)

#w, h = rows, cols;
#Matrix = [[0 for x in range(w)] for y in range(h)] 
#for  s in Matrix:
    #print(s)