#!/usr/bin/env python
# coding: utf-8

# # Task Scheduler Python 

# #### Description of the tasks 
# Every task in the input list has the following data fields:
# <br>*Task ID, Task Description, Task Duration in minutes, Multitasking, Dependencies, Status*
# 1. **Task ID [taskID]**: Unique task identifier which other tasks may reference (to deal with task dependencies).
# 2. **Task Description [desc]**. A short description of the task.
# 3. **Task Duration in minutes [time]**. Duration of the task in minutes. 
# 4. **Multitasking [multi]**. A boolean field that indicates whether or not the task allows for multitasking. If multitasking possible it can pick a task from independent task to do alongside.
# 5. **Dependencies [depends]**. This is a list of Task IDs indicating whether the current task cannot begin until all of its dependencies have been completed (e.g. one cannot eat gogigui unless one has already found a restaurant in Seoul, has arrived at a restaurant, has gotten a table, has ordered, etc.)
# 6. **Status [status]**. A task is one of these states: **0 for not-completed, 1 for completed** 

# In[1]:


#initializing hard coded data of tasks

#store activities with their tasks IDs that needs to be done to accomplish the activity
activityList = {"N Seoul Tower": ["t0", "t1", "t2"], "Eat Local Cuisine": ["t3","t4","t5"], 
                "Participate in Dance Competition" : ["t6", "t7", "t8"], 
                "Try a New Cafe" : ["t13","t14","t15"],
                "Networking with Professionals" : ["t9", "t10", "t12", "t11"]
               }

#store all activity-based tasks here
activityTasks = {"t0":{"desc": 'Exploring N Seoul tower', "time": 60, "multi": False, "depends": "t1", "status": 0},
    "t1" : {"desc": 'Hike up Namsan Park', "time": 30, "multi": True, "depends": None, "status": 0},
    "t2" : {"desc": 'Take Cable Car Down', "time": 20, "multi": False, "depends": "t0", "status": 0},
    "t3" : {"desc": 'Eat Bibimbap', "time": 30, "multi": False, "depends": "t4", "status": 0},
    "t4" : {"desc": 'Reach Damoa Foods', "time": 20, "multi": True, "depends": "t5", "status": 0},
    "t5" : {"desc": 'Call friends to meet for lunch', "time": 5, "multi": False, "depends": None, "status": 0},
    "t6" : {"desc": 'Reach Dance Theatre', "time": 20, "multi": True, "depends": "t7", "status": 0},
    "t7" : {"desc": 'Buy Dancing Costume', "time": 40, "multi": False, "depends": None, "status": 0},
    "t8" : {"desc": 'Perform Traditional Dance', "time": 25, "multi": False, "depends": "t6", "status": 0},
    "t9" : {"desc": 'Reach Tech Fair', "time": 25, "multi": True, "depends": "t11", "status": 0},
    "t10" : {"desc": 'Prepare Resume, Cover Letter', "time": 15, "multi": False, "depends": None, "status": 0},
    "t11" : {"desc": 'Suit up', "time": 20, "multi": False, "depends": "t10", "status": 0},
    "t12" : {"desc": 'Chat with Employers', "time": 30, "multi": False, "depends": "t9", "status": 0},
    "t13" : {"desc": 'Search online for a new cafe', "time": 5, "multi": False, "depends": None, "status": 0},
    "t14" : {"desc": 'Reach Cafe', "time": 20, "multi": True, "depends": "t13", "status": 0},
    "t15" : {"desc": 'Drink Specialty Coffee', "time": 20, "multi": True, "depends": "t14", "status": 0},
    }

#store all independent tasks here
#note: independent task refer to tasks that are not part of any activity-based
independentTasks = {"i0":{"desc": 'Exchanging Dollars to Won', "time": 20, "multi": False, "status": 0},
    "i1" : {"desc": 'Recharging T-Money card', "time": 5, "multi": False, "status": 0},
    "i2" : {"desc": 'Calling Mom', "time": 15, "multi": True, "status": 0},
    "i3" : {"desc": 'Listening to Millionaire Podcast', "time": 15, "multi": True, "status": 0},
    "i4" : {"desc": 'Create a music playlist', "time": 15, "multi": True, "status": 0},
    "i5" : {"desc": 'Find internships online', "time": 25, "multi": True, "status": 0},
    }


# In[2]:


#printing the tasks in a tabular format

from tabulate import tabulate #importing library to use tabulate() function

def printTable(data, keyTitle): #function to print data we fed in a tabular form
    rowValue = [() for x in range(len(data))] #creating an empty row
    headers = [] #array to hold headers picked from data
    column = 0 #column counter

    for key in data: #taking first object from our data which is the taskId 
        
        rowValue[column] = rowValue[column] + (key,) #adding taskId to the first column
        
        for subKey in data[key]: #for each object(taskID) we have more details like desc, time, etc.
            if column == 0: #adding desc, time etc. to headers
                headers.append(subKey)
            rowValue[column] = rowValue[column] + (data[key][subKey],) #storing value of header
        column+=1 #counter
        
    headers.insert(0, keyTitle) #adding header for the objects(taskID)
    print(tabulate(rowValue, headers, tablefmt="fancy_grid")) #printing the table

print("Let's take a look at your tasks table now\n>>> Table 1. Activity-based Tasks") #table caption
printTable(activityTasks, "Task ID") #calling the function to display activity tasks
for i in range(90): print("#", end = '') #adding some gap for visual purposes
print("\n>>> Table 2. Independent Tasks") #table caption
printTable(independentTasks, "TaskID") #printing table


# #### Task Priority Scheduler in Python 3, which receives the list of tasks above as input and returns an optimal task schedule for you to follow.

# In[3]:


activityName = [] #to store activites name
subTasks = [] #to store tasks under activities

for i in activityList: #iterating through hardcoded data fed about activities
    activityName.append(i) #storing activity names
    subTasks.append(activityList[i]) #storing tasks under activities
    
activityTime = [0 for i in range(len(subTasks))] #to store each activity total time

c = 0 #counter
for i in subTasks: #iterating through each task under one activity
    for j in i: #finding time for each task
        activityTime[c]+=activityTasks[j]["time"] #storing the time and summing
    c+=1 #counter


givenTime = 297 ### <<<<<<<<--------------------------------- INPUT available time(minutes) here !!!!!!!!!!!


totalTime = 0 #to store activity consumed total time
bestCombination = None #to find best combination of activity time to maximize usage
mx = 0 #to store max combination so far

def combinations(iterable, r): #this function is from the library
    #combinations('ABCD', 2) --> AB AC AD BC BD CD
    #combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

for i in range(1,len(activityTime)+1): #iterating through activity times and finding best combination
    comb = combinations(activityTime, i) #taking i number of activity times at a time
    
    for j in list(comb):
        totalTime = sum(j) #summing time of the combination of activities time
        if totalTime > mx and totalTime <= givenTime: #checking if the combination is doable in given time
            mx = totalTime #updating max value of combination
            bestCombination = list(j) #storing the best combination
        
        totalTime = 0

activitiesToDo = [] #to store the best combination of activities to do

print("You can accomplish following activties in", givenTime,"minutes.") #printing total time available

for k in bestCombination: #iterating through the best combination
    activitiesToDo.append(activityName[activityTime.index(k)]) #storing activity name to do
    print("> ",activityName[activityTime.index(k)], ", which will take",k, "minutes") #printing activity name+time
    
print("\nYou will still be left with", givenTime - sum(bestCombination), "minutes.") #printing remainder time


# In[4]:


indTime = [] #to store independent task times
for i in independentTasks: #iterating through independent tasks
    indTime.append(independentTasks[i]["time"]) #storing their task times
indName = [] #to store independent task names
for i in independentTasks: #iterating throught tasks
    indName.append(i) #storing their name


# In[5]:


'''
Function takes Task ID and executes the task, if any dependency then recursively executes itself on dependency
if dependency has a dependency then again recursively calls itself for it... and so on
''' 
def doTask(taskId): #function start
    global indTime #variable with independent task times
    global indName #varianle with independent task 
    mx = 0 #to store max combination of independent tasks
    totTime = 0 #total time of activity
    bestCombi = None #to store best combination
    dependency = activityTasks[taskId]["depends"] #finding dependency
    
    if activityTasks[taskId]["status"] == 0: #checking if task not completed
        if dependency != None: #checking if there is dependency
            if activityTasks[dependency]["status"] == 0: #checking if dependency already done
                doTask(dependency) #if dependency not completed then do it
        
        activityTasks[taskId]["status"] = 1 #after dependency done, do the task by updating status
        print("> ", activityTasks[taskId]["desc"]) #print the task
        
        if activityTasks[taskId]["multi"] == True: #checking if the task is multitaskable
            givenTime = activityTasks[taskId]["time"] #get total time of the task, so we can multitask

            for i in range(1,len(indTime)+1): #iterate through independent tasks time
                combi = combinations(indTime, i) #take i length combinations of tasks times
                for j in list(combi): #iterate through the combinations
                    totTime = sum(j) #sum them
                    if totTime > mx and totTime <=givenTime: #if they are doable within given time and they are new max
                        mx = totTime #updated max, as we want to maximize the use of multitaskable time
                        bestCombi = list(j) #update the best combination of independent tasks that can be done
            
            print("\tWhile doing the above task, you can multitask by:", end = '')
            for k in bestCombi: #taking each task from the best combination
                print("", independentTasks[indName[indTime.index(k)]]["desc"], end='.') #printing task desc, execute
                independentTasks[indName[indTime.index(k)]]["status"] = 1 #update task status
                indName.pop(indTime.index(k)) #remove task from the list of executable independent tasks
                indTime.pop(indTime.index(k)) #remove task from the list of executable independent tasks
            
            print(" ") #add new line
    
    else: #task is already completed do nothing
        return


# In[6]:


tasksToDo = [] #to store tasks to be done 

for act in activitiesToDo: #iterate through activites to do
    for i in activityList[act]: #find tasks under the activity
        tasksToDo.append(i) #store tasks

print("Follow the step-by-step instruction to accomplish activities in given", givenTime,"minutes\n") #print avialable time

for task in tasksToDo: #iterate through tasks to do list
    doTask(task) #execute tasks

print("\nYou will be left with", givenTime - sum(bestCombination), "minutes to use as you may.")


# In[7]:


print("Let's take a look at your updated task table now\n>>> Table 3. Activity-based Tasks - Updated") #table caption
printTable(activityTasks, "Task ID") #calling the function to display activity tasks
for i in range(90): print("#", end = '') #adding some gap for visual purposes
print("\n>>> Table 4. Independent Tasks - Updated") #table caption
printTable(independentTasks, "TaskID") #printing table


# #### How does this scheduler work?
# 
# 1. Input Activity-based tasks and Independent Tasks, we have to let the program know what tasks is each activity composed of, as we seek to execute activity by activty and we will multitask by doing an independent task while doing an activity-based task. 
#  1. Eg. While drinking coffee(activity-based task) multitask by calling mom(independent task)
# 
# 2. When the data is input, it generates a table which shows the fed data
# 
# 3. We should give a value to *givenTime* variable, which is the total available time we have in hande
#  
# 4. The program creates a list of total time of each activity
# 
# 5. The program considers the toal available time we have and finds the best combination of activities we can accomplish by taking the sum of their time that will use most of available time.
# 
# 6. After getting the activities that can make most out of the available time, it *prioritizes* the actvity in descending order of their total time. That way we execute activity from the list which takes the max time first and then next max... and so on until all are sorted in that manner.
# 
# 7. Now we have the activity execution order. The program looks at the activity and find the tasks that need to completed for the activity to be accomplished.
#  1. It runs the tasks listed and if the task has a dependency then it will run its dependency first and then the task
#  2. If dependency has a dependency then it will recursively run the dependency of dependency that needs to be executed.
# 
# 8. While executing tasks for the activity, if the task is multitaskable then the program finds the time of the task and finds the best combination of independent tasks that will make the most out of the multitaskable time while *prioritizing* in descending order of independent task time.
# 
# 9. The program then outputs the step-by-step instructions to follow and shows the updated table.

# The algorithm makes the most out of available time to accomplish activities and by multitasking on an activity-based task with an independent task. It gives a proper step-by-step instruction to be executed
# 
# <br>
# The integer-operations are O(1) which can be neglected. The printTable() has nested for loops where the outer loop is executed number of tasks time and the inner is executed for each task "task details" times, which 5 for activity-based tasks and 4 for independent tasks. The combinations(iterable, c) function, which gives us time complexity θ [ c(n choose c) ], "n choose c" gives us how many times function yields & how many times the outer while loop is iterated. during every iteration atleast output tuple of length c is produced that gives us the extra component c. Also, other inner-loops will account O(c) for each outer iteration. Assuming that tuple creation will be O(c). Anyway it should follow Ω [ c(n choose c) ]. the integer operations are O(1) which can be neglected. The combinations() is called (total activities times) first to compute the activties to do for given available time. And then it is called for each activity-based task that is multitaskable and is executed independent tasks available times. Generating combinations can take a lot of time, if we were to put 100 element list, if someone puts 100 tasks or activties.

# ##### Thank You
