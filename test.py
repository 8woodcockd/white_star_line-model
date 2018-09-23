# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 17:38:49 2018

@author: Dean
"""

checked = [1,2,3,4,5]
#print(checked)
for i in range(1):
    if 0 in checked:
        print('in list')
    else:
        print('not in list')
checked.remove(checked[1])
print(checked)


      
# List of string 
listOfStrings = ['Hi' , 'hello', 'at', 'this', 'there', 'from']
'''
    check if element exist in list using 'in'
'''
if 'at' in listOfStrings :
    print("Yes, 'at' found in List : " , listOfStrings)
'''
    check if element NOT exist in list using 'in'
'''
if 'time' not in listOfStrings :
    print("Yes, 'time' NOT found in List : " , listOfStrings)