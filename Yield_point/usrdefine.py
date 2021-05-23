
'''
lots of general function 
'''

def findclosest(array,goal):
    try:
        gap_abs=[abs(goal-i) for i in array]
        index=gap_abs.index(min(gap_abs))
        value=array[index]
        return index
    except:
        raise TypeError("Wrong type for Inputs")

