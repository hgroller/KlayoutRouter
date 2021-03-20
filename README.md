# KlayoutRouter
Proof of Concept Router for Klayout.

All text locations must be on an int grid location
no float's at the present time
Layout is based on Matthias si4all dummy pdk

Router is based and the following  A* code
# Credit for this: Nicholas Swift
# as found at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
#Modifications by Ryan Collingwood, N/S/E/W Orthognal
#https://gist.githubusercontent.com/ryancollingwood/32446307e976a11a1185a5394d6657bc/raw/4a3a432554f038281cf17ffac5f7a6adddbe669c/astar.py

Code consist's of :
place both files in C:/Users/your_path/KLayout/pymacros and change your_path

Router.py -----  in sys.path.append("C:/Users/your_path/KLayout/pymacros") and change your_path													

AstarRouter.py

testroute.gds is the test gds file with Text placements

Load Router.py in the IDE with the testroute.gds file open

In AstarRouter.py you can play with blockages by adding 1's in the maze array

Have fun, Comments welcomed.
