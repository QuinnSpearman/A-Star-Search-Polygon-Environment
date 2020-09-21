#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame as pg
from scipy.spatial import distance
pg.init()


# In[2]:


# Defines the height and width of the environment
width = 1000
height = 600

# Initializes the font
font = pg.font.SysFont(None, 40)

# Initializes colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Function that resizes coordinates
def get_tuple(x, y):
    xFinal = (x / 50) * width
    yFinal = height - (height * (y / 30))
    return (int(xFinal), int(yFinal))

# Finds the slope of a line based on 2 points
def calculate_slope(lineStart, lineEnd):
    # Find the slope of the line
    numerator = (lineStart[1] - lineEnd[1])
    denominator = (lineStart[0] - lineEnd[0])
    lineSlope = numerator / denominator
    return lineSlope

# Calculates the b value of the slope equation
def calculate_b(m, point):
    x = point[0]
    y = point[1]
    b = m * (-1 * x) + y
    return b;

# Calculates the intercept point of 2 lines
def calculate_intercept_point(m1, m2, b1, b2):
    if m1 == m2 :
        return (-1, -1)
    
    xPoint = (b2 - b1) / (m1 - m2)
    yPoint = m1 * xPoint + b1
    
    if xPoint < 0 or yPoint < 0:
        return (-1, -1)
    
    return (xPoint, yPoint)

# Checks if the intercept of the line is within 2 points on the line
def check_if_intercept_on_segment(linePoint1, linePoint2, intersectionPoint):
    x1 = linePoint1[0]
    y1 = linePoint1[1]
    x2 = linePoint2[0]
    y2 = linePoint2[1]
    x3 = intersectionPoint[0]
    y3 = intersectionPoint[1]

    if y1 == y2:
        if (min(x1, x2) < x3 and x3 < max(x1, x2)):
            return True
    else:    
        if (min(x1, x2) < x3 and x3 < max(x1, x2)) and (min(y1, y2) < y3 and y3 < max(y1, y2)):
            return True
    return False


# Checks if a point is a valid destination from another point
def check_if_valid_destination(startPoint, endPoint, polygons, currentPolygon):
    startPointX = startPoint[0]
    startPointY = startPoint[1]
    endPointX = endPoint[0]
    endPointY = endPoint[1]
    
    # If the start point and the endpoint are in the current polygon being checked, check if the endpoint is a valid destination on the polygon
    if startPoint in currentPolygon and endPoint in currentPolygon:
        return check_if_valid_destination_on_polygon(startPoint, endPoint, currentPolygon)
    else:
        for polygon in polygons:
            for index in range(len(polygon)):
                # Stores the 2 points being investigated of the polygon
                polygonEdgePoint1 = polygon[index % len(polygon)]
                polygonEdgePoint2 = polygon[(index + 1) % len(polygon)]

                # Stores the individual x and y values of each polygon point
                xPolygonEdgePoint1 = polygonEdgePoint1[0]
                yPolygonEdgePoint1 = polygonEdgePoint1[1]
                xPolygonEdgePoint2 = polygonEdgePoint2[0]
                yPolygonEdgePoint2 = polygonEdgePoint2[1]

                # Stores the difference between the x values on the polygon edge
                polygonEdgeXDifference = xPolygonEdgePoint1 - xPolygonEdgePoint2
                # Stores the difference between the x values on the movement line
                movementLineXDifference = startPointX - endPointX
                
                # If both lines are vertical, continue to next iteration of loop
                if polygonEdgeXDifference == 0 and movementLineXDifference == 0:
                    continue
                # If the polygon edge is vertical, check if it intersects with the movement line
                elif polygonEdgeXDifference == 0:
                    if check_vertical_line_intersection(startPoint, endPoint, polygonEdgePoint1, polygonEdgePoint2):
                        return False
                # If the movement line is vertical, check if it intersects with the movement line
                elif movementLineXDifference == 0:
                    if check_vertical_line_intersection(polygonEdgePoint1, polygonEdgePoint2, startPoint, endPoint):
                        return False
                # Otherwise, if both lines are not vertical
                else:
                    # Get slope and b value of movement line
                    movementLineSlope = calculate_slope(startPoint, endPoint)#
                    movementLineB = calculate_b(movementLineSlope, startPoint)#
                    # Get slope and b value of polygon edge
                    polygonEdgeSlope = calculate_slope(polygonEdgePoint1, polygonEdgePoint2)#
                    polygonEdgeB = calculate_b(polygonEdgeSlope, polygonEdgePoint1)#
                    # Get the intersection point of both lines
                    intersectionPoint = calculate_intercept_point(movementLineSlope, polygonEdgeSlope, movementLineB, polygonEdgeB)#
                    
                    # Check if the intersection falls within the line segment
                    if check_if_intercept_on_segment(startPoint, endPoint, intersectionPoint):
                        if check_if_intercept_on_segment(polygonEdgePoint1, polygonEdgePoint2, intersectionPoint):
                            return False
                        
        return True
                
                
# Checks to see if a normal line intersects with a vertical line
def check_vertical_line_intersection(startPointNormal, endPointNormal, startPointVertical, endPointVertical):
    # Get slope for movement line
    slope = calculate_slope(startPointNormal, endPointNormal)
    # Get b for movement line
    b = calculate_b(slope, startPointNormal)
    # Get the intercept point
    yInterceptPoint = slope * startPointVertical[0] + b
    xInterceptPoint = startPointVertical[0]
    interceptPoint = (xInterceptPoint, yInterceptPoint)

    y1Vert = startPointVertical[1]
    y2Vert = endPointVertical[1]
    
    # If the intercept point is between y1 and y2
    if min(y1Vert, y2Vert) < yInterceptPoint and yInterceptPoint < max(y1Vert, y2Vert):
        x1 = startPointNormal[0]
        y1 = startPointNormal[1]
        x2 = endPointNormal[0]
        y2 = endPointNormal[1]

        interceptPoint = (xInterceptPoint, yInterceptPoint)
        # If the intersection is on the line segment
        if check_if_intercept_on_segment(startPointNormal, endPointNormal, interceptPoint):
            return True
        
    return False            
            
            
            
        
def check_if_valid_destination_on_polygon(startPoint, endPoint, currentPolygon):
    
    
    startPointIndex = currentPolygon.index(startPoint)
    endPointIndex = currentPolygon.index(endPoint)
        
    if (startPointIndex == 0 and endPointIndex == len(currentPolygon) - 1) or (endPointIndex == 0 and startPointIndex == len(currentPolygon) - 1):
        return True
    elif abs(startPointIndex - endPointIndex) == 1:
        return True
    else:
        return False
            

def get_current_polygon(point, polygons):
    for polygon in polygons:
        if point in polygon:
            return polygon
    return (-1, -1)

def actions(startPoint, points, polygons):
    
    validDestinations = []
    
    currentPolygon = get_current_polygon(startPoint, polygons)
    
    for endPoint in points:
        if check_if_valid_destination(startPoint, endPoint, polygons, currentPolygon):
            validDestinations.append(endPoint)
            
    return validDestinations

        
def h(n, goal): 
    return distance.euclidean(n, goal)
        
def g(nStart, nFinish):
    return distance.euclidean(nStart, nFinish)

# A star Search function
def a_star_search(start, goal, points, polygons):
    # Initialize closed list and priority queue
    closedList = []
    priorityQueue = []
    
    # New priority queue structure: {'f': , 'point', 'goal', 'g', 'parent'}
    
    # Appends the start node to the priority queue
    #priorityQueue.append({'f': h(start, goal) , 'node': Node(start, goal, 0, None)})
    priorityQueue.append({'f': h(start, goal) , 'point': start, 'g': 0, 'parent': None})
    
    # While the priority queue isn't empty
    while len(priorityQueue) > 0:
        # Pop the top element out of the priority queue and assign it to current node
        currentNode = priorityQueue.pop(0)
        # If the current node is the goal node
        if currentNode['point'] == goal:
            return currentNode
        # Get the set of all of the possible destinations from the current node
        validDestinations = actions(currentNode['point'], points, polygons)
        # For every destination in valid destinations
        for destination in validDestinations:
            foundGreaterMatch = False
            if destination in closedList:
                continue
                    
            # Add distance from current node to the next node
            gCost = currentNode['g'] + g(currentNode['point'], destination)
            # Create a new node and assign g cost as the total distance traveled to this point
            newNode = {'f': gCost + h(destination, goal), 'point': destination, 'g': gCost, 'parent': currentNode}
            # For every node in the priority queue
            for priorityQueueNode in priorityQueue:
                # If the point of the new node equals a point on a node in the priority queue
                if newNode['point'] == priorityQueueNode['point']:
                    # If the g value of the new node is less than the value of the node in the queue, remove the old value
                    if newNode['g'] < priorityQueueNode['g']:  
                        priorityQueue.remove(priorityQueueNode)
                        break
                    else:
                        foundGreaterMatch = True
            # If the g value wasn't greater, insert the new value into the priority queue
            if not foundGreaterMatch:
                priorityQueue.append(newNode)
                priorityQueue.sort(key = key_function)
        
        # Put the current node in the closed list
        closedList.append(currentNode['point'])    
        
        
        
        
    
    
    
    
    #print(priorityQueue)
    
    
def key_function(e):
    return e['f']
    
def start_text(location):
    screen_text = font.render("S", True, black)
    gameDisplay.blit(screen_text, [location[0] - 35, location[1] - 12])
    
def goal_text(location):
    screen_text = font.render("G", True, black)
    gameDisplay.blit(screen_text, [location[0] + 23, location[1] - 12])
    
#def goal_text
        
        
        
    
    


# In[3]:


start = get_tuple(6, 3)
goal = get_tuple(43, 20)

polygon1 = [get_tuple(7, 1), get_tuple(7, 6), get_tuple(24, 6), get_tuple(24, 1)]
polygon2 = [get_tuple(7, 10), get_tuple(6,16), get_tuple(12,21), get_tuple(16, 16), get_tuple(13, 9)]
polygon3 = [get_tuple(16, 9), get_tuple(18, 17), get_tuple(20, 9)]
polygon4 = [get_tuple(21, 14), get_tuple(21,21), get_tuple(25, 22), get_tuple(28, 18)]
polygon5 = [get_tuple(25, 11), get_tuple(30, 7), get_tuple(27, 4)]
polygon6 = [get_tuple(29, 10), get_tuple(29, 21), get_tuple(36, 21), get_tuple(36, 10)]
polygon7 = [get_tuple(33, 3), get_tuple(33, 7), get_tuple(37, 9), get_tuple(40, 7), get_tuple(40, 2), get_tuple(37, 1)]
polygon8 = [get_tuple(37, 19), get_tuple(40, 21), get_tuple(42, 19), get_tuple(41, 8)]

polygons = [polygon1, polygon2, polygon3, polygon4, polygon5, polygon6, polygon7, polygon8]

points = polygon1 + polygon2 + polygon3 + polygon4 + polygon5 + polygon6 + polygon7 + polygon8 
points.append(goal)

path = a_star_search(start, goal, points, polygons)


# In[4]:


solutionPoints = []
currNode = path
while currNode != None:
    solutionPoints.append(currNode['point'])
    currNode = currNode['parent']


# In[5]:


start = get_tuple(6, 3)
goal = get_tuple(43, 20)
    
pg.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
gameDisplay = pg.display.set_mode((width, height))

pg.display.set_caption('A* Search')

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()


    gameDisplay.fill(white)
    
    for polygon in polygons:
        pg.draw.lines(gameDisplay, black, True, polygon, 2)
    
    pg.draw.circle(gameDisplay, black, start, 3)
    pg.draw.circle(gameDisplay, black, goal, 3)
    
    pg.draw.lines(gameDisplay, red, False, solutionPoints, 5)
    
    start_text(start)
    goal_text(goal)

    pg.display.update()

pg.quit()
quit()


# In[ ]:




