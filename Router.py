# Enter your Python code here
#Python Proof of Concept for A* Routing
#Tracy Groller 3/19/21
#Below Code find's all Text and Routes Point to Point
#ToDo: Vertical and Horizontal metals
#          Drop vias at intersection
#          Add Maze array definition based on the Border Layer
#    
import pya
import array
import sys
import math
from importlib import reload
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
texts = 0
layer_info = LayerInfo.new(13,0)
layer = layout.layer(layer_info) 
iter = layout.begin_shapes(cv.cell_index, layer)
if iter.shape().is_box():
  ux =  iter.shape().box.right
  uy =  iter.shape().box.top

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
     #Test Print
     #print("Text In Cell :" + iter.cell().name + ": " + string + " " +  str(x) + ","+ str(y))
  iter.next()

srt = sorted(coords)
print("The Array is: ", srt)

#Remove Duplicates from text list
strlst = sorted(list(dict.fromkeys(strlst)))

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


layer_info = LayerInfo.new(9,0)
layer_index = layout.layer(layer_info) 

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

#Filter the list to Search the text list
#For A* Routing 
#This works for 2 pins only at the present time
#All placements of Text needs to be centerd in via 
#All placements of Text need too be on a int no floats.

pathbuild = []

for search in strlst: 
  filtered = list(filter(lambda x:x[0]==search,srt))
  print('The filtered list for is: ' , filtered[0]) 
  wd = .3
  lay = 9
  lc1  = math.ceil(int(filtered[0][1]/1000))
  lc2  = math.ceil(int(filtered[0][2]/1000))
  lc3  = math.ceil(int(filtered[1][1]/1000))
  lc4  = math.ceil(int(filtered[1][2]/1000))
  loc1 = (lc1,lc2)
  loc2 = (lc3,lc4)
  pth  = AstarRouter.main(loc1,loc2)
  crd = coords(pth)
  create_path(crd,wd,lay)
 
 

    



