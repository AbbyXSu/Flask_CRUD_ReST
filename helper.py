#Adding Items
#To implement this feature we need two things:
#A helper function that contains business logic to add a new element in the database
#A route that should be called whenever a particular HTTP endpoint is hit

#This function establishes a connection with the database and executes an insert query. 
#It returns the inserted item and its status.


import sqlite3

DB_Path = "./todo_service_flask/todo.db"
NOTSTARTED = "Not started"
INPROGRESS ="In Progress"
COMPLETED = "Completed"

def add_to_list(item):
    try:
        conn =sqlite3.connect(DB_Path)
    #ONCE A CONNECTION HAS BEE NESTABLISHED, WE USE CURSOR OBJECT TO EXECUTE QUERIES
    # an Cursor object is a class object, it allows the code to access appointed database via a connection, it has to be bound by a connection with the SQL database
    #cursor() method: they are bound to the connection and all the commands are executed in the context of the database session wrapped by the connection. 
        c = conn.cursor()
    # here the cursor method are execute to insert items and status in the related columns in the database
        c.execute(f'insert into items(item, status) values("{item}","{NOTSTARTED}")')
    # we commit to save change
        conn.commit()
        return {"item":item, "status":NOTSTARTED}
    # except sqlite3.IntegrityError as e:(tried inserting a unque constraint)
    #     print('integrity error', e)
    #     raise Exception409 Conflict
    except Exception as e:
        print("error",e)
        return None

#add_to_list('hello world') to test


#Retrieving All Items (Get information of the items)


def get_all_items():
    try:
        conn=sqlite3.connect(DB_Path)
        c= conn.cursor()
#This function establishes a connection with the database and creates a SELECT query
        c.execute("select * from items")
#c.fetchall(). This returns all records returned by the SELECT query. If we are interested in only one item we can instead call c.fetchone().
        rows = c.fetchall()
#Our method, get_all_items returns a Python object containing 2 items:
#The number of items returned by this query
#The actual items returned by the query
        return {"count": len(rows),"items":rows}
    except Exception as e:
        print ("error",e)
        return None

#Getting a individual Item

def getone_item(item):
    try:
        conn=sqlite3.connect(DB_Path)
        c=conn.cursor()
#This function establishes a connection with the database and creates a SELECT query
        c.execute("select status from items where item ='%s'" % item)
        status =c.fetchone()[0]
        return status
    except Exception as e:
        print("error:",e)
        return None
    
#Updating Items
# here I will update the status of the items by setting an function
def update_status(item,status):
#make sure the value of teh status is valid
    if (status.lower().strip()== "not started"):
        status = NOTSTARTED
    elif (status.lower().strip() == "in progress"):
        status = INPROGRESS
    elif (status.lower().strip() == "completed"):
        status = COMPLETED
    else:
        print ("invalid Status: " + status)
        return None
#here the code will execute the update of the database
    try:
        conn =sqlite3.connect(DB_Path)
        c = conn.cursor()
        c.execute("update items set status =? where item=?",(status,item))
        conn.commit()
        return {item:status}
    except Exception as e:
        print("Error", e)
        return None

def delete_item(item):
    try:
        conn=sqlite3.connect(DB_Path)
        c=conn.cursor()
        c.execute("delete from items where item =?",(item,))
#note that (item,) is not a typo. We need to pass execute() a tuple even if there is only one item in the tuple.
# Adding the comma forces this to become a tuple.
        conn.commit()
        return {"item":item, 'message':'deleted'}
    except Exception as e:
        print ("Error:", e )
        return None