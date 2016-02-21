'''
Now that we are out of the review phase, you will be providing me with a 
complete program (no more templates).  Remember, I want to be able to run "Python 
yourprogram.py" and get the result.  The score will be determined not just on 
whether or not you get the proper output, but how you get there.

Write a software program that does all of the following:

Loads in the data from cars.data.csv.  The data can be stored anyway you choose, 
in any data structure you choose (probably a list of some kind).  The data should 
load on start-up by referencing a file path, or even better, a file picker dialog 
box.

In the main portion of your program you should run the following operations and 
print the result to the console (except number 4).  How you achieve this is up 
to you.  However, operations need to be performed on the data itself (don't 
hard code the solution).

    -Print to the console the top 10 rows of the data sorted by 'safety' in 
    descending order
    
    -Print to the console the bottom 15 rows of the data sorted by 'maint' in 
    ascending order

    -Print to the console all rows that are high or vhigh in fields 'buying', 
    'maint', and 'safety', sorted by 'doors' in ascending order.  Find these 
    matches using regular expressions.
    
    -Save to a file all rows (in any order) that are: 'buying': vhigh, 'maint': 
    med, 'doors': 4, and 'persons': 4 or more.  The file path can be a 
    hard-coded location (name it output.txt) or use a dialog box.  

Your code needs to be able to handle exceptions.  It should handle all data as 
specified by the data definition document from Lesson 2, and throw some kind of 
error when it encounters data that doesn't match that format.  To test this, I 
will add the line 'vlow, vlow, 1, 1, vbig, vhigh' to the .csv file.  Your 
program should gracefully handle this line in all cases from the previous part.

Going forward, code style will count a little bit.  So make sure it is readable 
and I can understand it.  Also, there are a few ways you can approach this 
assignment.  Ideally, you will create functions that can return the data in 
different ways, not just do what I am asking for in part 2.  For example, 
consider if I asked for something in a different order, how hard would it be to
 make that change in your code?
'''
import Tkinter
import tkFileDialog
import pandas as pd

root = Tkinter.Tk()
root.withdraw()

car_file = tkFileDialog.askopenfilename(parent=root)

car_data = pd.read_csv(car_file, header=None)

car_data.columns = ['buying_price','maint_price','doors',
                    'persons','trunk_size','safety','class']

general_rank = {'low':0, 'med':1, 'high':2, 'vhigh':3}
door_rank = {'2':0, '3':1, '4':2, '5more':3}
persons_rank = {'2':0, '4':1, 'more':2}
trunk_rank = {'small':0, 'med':1, 'big':2}
safety_rank = {'low':0, 'med':1, 'high':2}

error1 = [i for i in car_data['buying_price'] if i not in general_rank]
error2 = [i for i in car_data['maint_price'] if i not in general_rank]
error3 = [i for i in car_data['doors'] if i not in door_rank]
error4 = [i for i in car_data['persons'] if i not in persons_rank]
error5 = [i for i in car_data['trunk_size'] if i not in trunk_rank]
error6 = [i for i in car_data['safety'] if i not in safety_rank]

errors = (error1, error2, error3, error4, error4, error5, error6)

if __name__ == "__main__":

    for error in errors:
        if len(error) >= 1:
            raise NameError('invalid data')
        
        
    car_data_by_safety = car_data.iloc[1:10]
    car_data_by_safety['safety_rank'] = car_data_by_safety['safety'].map(general_rank)
    car_data_by_safety = car_data_by_safety.sort_values(by='safety_rank', ascending=False)
    
    print car_data_by_safety
    
    car_data_by_maint = car_data.iloc[-15:]
    car_data_by_maint['maint_rank'] = car_data_by_maint['maint_price'].map(general_rank)
    car_data_by_maint = car_data_by_maint.sort_values(by='maint_rank')
    
    print car_data_by_maint  
    
    car_data_by_doors = car_data
    
    car_data_by_doors['high_buy'] = car_data_by_doors['buying_price'].str.contains('v?high$')
    car_data_by_doors['high_maint'] = car_data_by_doors['maint_price'].str.contains('v?high$')
    car_data_by_doors['high_safe'] = car_data_by_doors['safety'].str.contains('v?high$')            
    
    car_data_by_doors = car_data_by_doors[(car_data_by_doors['high_buy'] == True) &
                                          (car_data_by_doors['high_maint'] == True) &
                                           (car_data_by_doors['high_safe'] == True)]
    
    car_data_by_doors['door_rank'] = car_data_by_doors['doors'].map(door_rank)
    car_data_by_doors = car_data_by_doors.sort_values(by='door_rank')
    
    print car_data_by_doors
    
    
    """  
        -Save to a file all rows (in any order) that are: 'buying': vhigh, 'maint': 
        med, 'doors': 4, and 'persons': 4 or more.  The file path can be a 
        hard-coded location (name it output.txt) or use a dialog box.  
    """
    
    car_data_output = car_data[(car_data['buying_price'] == 'vhigh') &
                                (car_data['maint_price'] == 'med') &
                                (car_data['doors'] == '4') &
                                ((car_data['persons'] == '4') | (car_data['persons'] == 'more'))]
    car_data_output.to_csv('car_output.csv')