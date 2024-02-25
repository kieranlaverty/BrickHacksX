
def centered_pose(right, left):
    if not (left == None or right == None):
        xl = left.landmark[9].x
        yl = left.landmark[9].y


        x = right.landmark[9].x
        y = right.landmark[9].y
        if (xl < .25 and yl < .25) and (x > .75 and y > .75):
            print("centered_pose")

def anti_superman_pose(right, left):
    if not (left == None or right == None):
        xl = left.landmark[9].x
        yl = left.landmark[9].y


        x = right.landmark[9].x
        y = right.landmark[9].y
        if (x < .25 and y < .25) and (xl > .75 and yl > .75):
            print("anti_superman_pose")

def superman_pose(right, left):
    if not (left == None or right == None):
        xl = left.landmark[9].x
        yl = left.landmark[9].y


        x = right.landmark[9].x
        y = right.landmark[9].y
        if (xl < .25 and yl < .25) and (x > .75 and y > .75):
            print("superman_pose")

def t_pose(right, left):
    if not (left == None or right == None):
        xl = left.landmark[9].x
        yl = left.landmark[9].y


        x = right.landmark[9].x
        y = right.landmark[9].y
        if xl < .25 and x > .75 :
            print("T_pose")
            

def reverse_t_pose(left, right):
    if not (left == None or right == None):
        xl = left.landmark[9].x
        yl = left.landmark[9].y


        x = right.landmark[9].x
        y = right.landmark[9].y
        if xl < .25 and x > .75:
            print("reverse_T_pose")
    
    
    """ if not (left == None):
        x = left.landmark[9].x
        y = left.landmark[9].y
        if x < .25:
            print("yes")
        if x > .75:
            print("no")
    
    if not (right == None):
        x = right.landmark[9].x
        y = right.landmark[9].y
        if x < .25:
            print("yes")
        if x > .75:
            print("no") """