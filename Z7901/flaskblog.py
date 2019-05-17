### Example inspired by Tutorial at https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
### However the actual example uses sqlalchemy which uses Object Relational Mapper, which are not covered in this course. I have instead used natural sQL queries for this demo. 

from flask import Flask, render_template, url_for, flash, redirect ,request
from forms import RegistrationForm, BlogForm, CarInfoForm, RatingForm, WishlistForm, InspectionForm
import datetime
import mysql.connector
from util import json_io
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


hostname = 'localhost'
username = 'root'
password = ''
database = '7901'
cnn  =mysql.connector.connect(host=hostname, user=username, passwd=password, db=database )
#conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)

userio = json_io()
currentUser=0

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        currentUser=userio.read()
        if currentUser == 0:
            return redirect(url_for('login_tmp', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

#Turn the results from the database into a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database )
        c = conn.cursor()
        
        #Add the new blog into the 'blogs' table
        query = 'insert into users VALUES (' + "'" + form.username.data + "',"  + "'" + form.email.data + "'," + "'" + form.password.data + "'" + ')' #Build the query
        c.execute(query) #Execute the query
        conn.commit() #Commit the changes

        flash(f'Account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)



@app.route("/", methods=['GET'])
def landing():
    return render_template('landing.html');

@app.route("/login", methods=['GET','POST'])
def login_tmp():
    if request.method == 'POST':
        gCurrentUser={}
        gCurrentUser['currentUser']=request.form.get("userId")
        userio.save_userid(gCurrentUser)
        return redirect(url_for('Posts'))        
    return render_template('login.html');
#Inspection    
@app.route("/inspection",methods=['GET', 'POST'])
def Inspect():
    if request.method == 'GET':

        conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database )
        c = conn.cursor()
        c.execute("SELECT * FROM Inspection")
        inspects = c.fetchall()
        return render_template('inspection.html', inspects=inspects)
    else:
        conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database )
        postid = (request.form.get("Postid"))
        inspect_id = (request.form.get("Inspect_id"))
        date = (request.form.get("Date"))
        location = (request.form.get("Location"))
        if_booked = (request.form.get("If_booked"))
        # #Display all blogs from the 'blogs' table
        
        cond = 'WHERE '
        count = 0

        if inspect_id is not None:
            if(count>0):
                cond += " AND "
            count = count+1
            cond=cond + "Inspect_id = '"+ inspect_id+"'"
        if location is not None:
            if(count>0):
                cond += " AND "
            count = count+1
            cond=cond + "LOWER(Location) LIKE '%"+ location.lower() +"%'"
        if postid is not None:
            if(count>0):
                cond += " AND "
            count = count+1
            cond=cond + "Postid = '"+ postid+"'"
        if date is not None:
            if(count>0):
                cond += " AND "
            count = count+1
            if(date=="1"):
                cond=cond + "Date < 20190901 AND Date>= 20190801" 
            elif(date=="2"):
                cond=cond + "Date < 20191001 AND Date>= 20190901" 
            elif(date=="3"):
                cond=cond + "Date < 20191101 AND Date>= 20191001" 
            elif(date=="4"):
                cond=cond + "Date < 20191201 AND Date>= 20191101"
            elif(date=="5"):
                cond=cond + "Date < 20200101 AND Date>= 20191201"           
        if if_booked is not None:
            if(count>0):
                cond += " AND "
            count = count+1
            if(if_booked=="Yes"):
                cond=cond + "If_booked = '1'" 
            elif(if_booked=="Not Yet"):
                cond=cond + "If_booked = '0'" 

        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("SELECT * FROM Inspection " + cond)
        inspects = c.fetchall()
        print(inspects)
        return render_template('inspection.html', inspects=inspects)
#wishlist
@app.route("/wishlist", methods=['GET', 'POST'])
def wishlist():
    if request.method == 'GET':
        conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
        c = conn.cursor()
        c.execute("SELECT W.*, P.Postid FROM WishList W,Post P WHERE W.Uid = P.Uid")
        wishlist = c.fetchall()

        return render_template('wishlist.html', title='WishList', wishlist=wishlist)
    else:
        conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
        uid = (request.form.get("Uid"))
        wishid = (request.form.get("Wishid"))
        postid = (request.form.get("Postid"))
        # #Display all blogs from the 'blogs' table
        
        cond = 'WHERE '
        count = 0

        if (not (uid is None)):
            if(count>0):
                cond += " AND "
            count = count+1
            cond=cond + "Uid = " + uid  
        if (not (wishid is None)):
            if(count>0):
                cond += " AND "
            count = count+1
            cond=cond + "Wishid = "+ wishid 

        if (not (postid is None)):
            if(count>0):
                cond += " AND "
            count = count+1
            cond=cond + "Postid = "+ postid         
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("SELECT W.*, P.Postid FROM WishList W,Post P " + cond)
        wishlist = c.fetchall()
        return render_template('wishlist.html', wishlist=wishlist)

@app.route('/add_wishlist', methods=['GET', 'POST'])
def add_wish():
    # number of wish
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM WishList")
    wishnum = c.fetchall()
    wishnum = int(wishnum[0][0])+1      
    if request.method == 'GET':
        form=WishlistForm()
        conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database )
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("SELECT * FROM Wishlist")
        wishlist = c.fetchall()
        return render_template('add_wishlist.html', title='Wishlist', wishlist=wishlist,form=form)


    elif request.method == 'POST':
        form = WishlistForm(request.form)
        uid=request.form.get("uid")
        c.execute("SELECT * FROM WishList W WHERE W.Uid="+(uid))
        results = c.fetchall()
     
        if form.validate_on_submit():
            uid = form.uid.data
            postid = form.postid.data

            c.execute('insert into WishList W,Post P' + uid, postid)
            print('insert into WishList W,Post P' + uid, postid)
            conn.commit()

            flash(f'New Wishlist has been created!.', 'success')
            return redirect(url_for('wishlist.html'))
        return render_template('add_wishlist.html', title='New WishList', form=form)


# def delete_wish(wishid):
#     conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)

#     cursor = conn.cursor()
#     cursor.execute('DELETE FROM WishList WHERE Wishid='+ wishid )
#     flash(f'Wishlist{wform.wishid.data}has been deleted.', 'success') 
#     conn.commit() 
#     return redirect(url_for('wishlist'))

@app.route("/rating", methods=['GET', 'POST'])
def rating():
    if request.method == 'GET':
        conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database )
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("SELECT * FROM Rating")
        rating = c.fetchall()
        return render_template('rating.html', title='Rating', rating=rating)
    else:
        conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
        uid = (request.form.get("Uid"))
        rid = (request.form.get("Rid"))
        comment = (request.form.get("Comment"))
        date_post = (request.form.get("Date_post"))
        stars = (request.form.get("Stars"))

        # #Display all blogs from the 'blogs' table
        
        cond = 'WHERE '
        count = 0
 
        if (not (uid is None)):
            if(count>0):
                cond += " AND "
            count = count+1
            cond=cond + "Uid = " + uid  
        if (not (rid is None)):
            if(count>0):
                cond += " AND "
            count = count+1
            cond=cond + "Rid = "+ rid  
        if (not (comment is None)):
            if(count>0):
                cond += " AND "
            count = count+1
            cond=cond + "LOWER(Comment) LIKE '%"+ comment.lower() +"%'"
        if (not (date_post is None)):
            if(count>0):
                cond += " AND "
            count = count+1
            if(date_post=="2017"):
                cond=cond + "Date_post >= 20170101  AND Date_post < 20180101" 
            elif(date_post=="2018"):
                cond=cond + "Date_post >= 20180101  AND Date_post < 20190101" 
            elif(date_post=="2019"):
                cond=cond + "Date_post >= 20190101  AND Date_post < 20200101"  
        if (not (stars is None)):
            if(count>0):
                cond += " AND "
            count = count+1
            cond=cond + "Stars = "+ stars 

        conn.row_factory = dict_factory
        c = conn.cursor()

        c.execute("SELECT * FROM Rating " + cond)
        rating = c.fetchall()
        return render_template('rating.html', rating=rating)

@app.route('/edit_rating', methods=['GET', 'POST'])
def edit_rating():
    if request.method=="GET":

        form = RatingForm()
        conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database) 
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("SELECT * FROM Rating")            
        rating = c.fetchall()
        return render_template('edit_rating.html', title='edit_rating', form=form) 
    # form = RatingForm(request.form)
    # conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    # uid = (request.form.get("Uid"))
    # rid = (request.form.get("Rid"))
    # comment = (request.form.get("Comment"))
    # date_post = (request.form.get("Date_post"))
    # stars = (request.form.get("Stars"))
    # #Display all rid 
    # #conn.row_factory = lambda cursor, row: row[0]
    # c = conn.cursor()

    # c.execute("SELECT COUNT(*) FROM Rating")
    # ratingnum = c.fetchall()
    # ratingnum = int(ratingnum[0][0])+1

    # # all uid list
    # if (request.method == 'POST'):
    #     form = RatingForm()
    #     if form.validate_on_submit():

    #         comment= form.comment.data
    #         stars = form.stars.data
    
    #         c.execute("UPDATE Rating SET Comment = " + comment.lower() + "WHERE Rid = " + rid )
    #         conn.commit()
    #         flash(f'Rating has been edited!.', 'success')
    #         return redirect(url_for('rating')) 
    #     return render_template('edit_rating.html', title='New Rating', form=form)



# @app.route("/rating/<string:rid>", methods=['POST'])
# def delete_rating(rid):
#     conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
#     conn.row_factory = lambda cursor, row: row[0]
#     c = conn.cursor()
#     c.execute('DELETE FROM Rating WHERE Rid='+rid)
#     conn.commit() 
#     return redirect(url_for('rating'))
  
    
@app.route("/Posts",methods=['GET', 'POST'])
def Posts():
    if request.method == 'GET':
        # conn = sqlite3.connect('car.db')

        conn = mysql.connector.connect()
        #Display all blogs from the 'blogs' tablehost=hostname, user=username, passwd=password, db=database
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("SELECT * FROM Post")
        posts = c.fetchall()
        # print(posts[7][13])
        return render_template('Posts.html', posts=posts)
    else:
        conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
        carType = (request.form.get("carType"))
        price = (request.form.get("price"))
        brand = (request.form.get("brand"))
        manuYear = (request.form.get("manuYear"))
        location = (request.form.get("location"))
        stars = (request.form.get("stars"))
        # #Display all blogs from the 'blogs' table
        
        cond = 'WHERE '
        count = 0
        if (not (carType is None)):
            count = count+1
            cond=cond + "LOWER(Car_type) LIKE '%"+ carType.lower() +"%'"
        if (not (brand is None)):
            if(count>0):
                cond += " AND "
            count = count+1
            cond=cond + "LOWER(Brand) LIKE '%"+ brand.lower() +"%'"
        if (not (location is None)):
            if(count>0):
                cond += " AND "
            count = count+1
            cond=cond + "LOWER(Location) LIKE '%"+ location.lower() +"%'"
        if (not (stars is None)):
            if(count>0):
                cond += " AND "
            count = count+1
            cond=cond + "Stars = '"+ stars[1]+"'"
        if (not (price is None)):
            if(count>0):
                cond += " AND "
            count = count+1
            if(price=="p0"):
                cond=cond + "Price < 2000" 
            elif(price=="p2"):
                cond=cond + "Price < 4000 AND Price>= 2000" 
            elif(price=="p4"):
                cond=cond + "Price < 6000 AND Price>= 4000" 
            elif(price=="p6"):
                cond=cond + "Price >= 6000"
        if (not (manuYear is None)):
            if(count>0):
                cond += " AND "
            count = count+1
            if(manuYear=="y1"):
                cond=cond + "manu_year like '19%'" 
            elif(manuYear=="y2"):
                cond=cond + "manu_year like '200%'" 
            elif(manuYear=="y3"):
                cond=cond + "manu_year like '201%'" 
           
        # print(cond)
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("SELECT * FROM Post " + cond)
        posts = c.fetchall()
        return render_template('Posts.html', posts=posts)
#get /Posts/<name> data: {name :}
@app.route('/Posts/<string:name>')
def get_post(name):
    currentUser=userio.read()
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    #Display all blogs from the 'blogs' table
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("SELECT P.*,U.First_name, U.Last_name FROM Post P,Seller S,User U WHERE P.Uid=S.Uid AND S.Uid=U.Uid AND P.Postid="+name)
    post = c.fetchone()
    return render_template('show.html',post=post, currentUser=currentUser)

@app.route('/Posts/<string:name>/edit', methods=['GET', 'POST'])
def edit_post(name):
    currentUser=userio.read()
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    #Display all usernames stored in 'users' in the Username field
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    if (request.method == 'POST'):
        form = CarInfoForm(request.form)
        # user
        c.execute("SELECT Uid,First_name,Last_name FROM User WHERE Uid="+str(currentUser))
        results = c.fetchall()
        users = [(results.index(item), item) for item in results]
        form.username.choices = users
        # specialist
        c.execute("SELECT * FROM Specialist")
        specialist_res = c.fetchall()
        specialist = [(specialist_res.index(item), item) for item in specialist_res]
        form.specialist.choices = specialist
        form.stars.choices = ((0,(1)),(1,(2)),(2,(3)))
        
        if(form.validate_on_submit()):
            specialist = form.specialist.choices[form.specialist.data][1]
            stars = form.stars.choices[form.stars.data][1]
            user =  users[form.username.data][1]
            title = form.title.data
            content = form.content.data
            location= form.location.data
            color   = form.color.data
            carType =form.carType.data
            brand  = form.brand.data
            price  = form.price.data
            manuYear = form.manuYear.data
            image = form.image.data
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
            # Add the new Post into the 'blogs' table in the database
            title = title.replace("'","''")
            content = content.replace("'","''")
            # print("==========image========",image)
            query = 'UPDATE Post SET Date_post='+"'"+timestamp+"'" +',Title='+"'" +title+"'" +',Description='+"'" +content+"'" +',Location='+"'" +location+"'" +',Color='+"'" +color+"'" +',Car_type='+"'" +carType+"'" +',Brand='+"'" +brand+"'" +',Price='+str(price)+',manu_year='+str(manuYear)+',Sid='+str(specialist[0])+',Stars='+str(stars) + ',Imageid=' +str(image)+' WHERE Postid='+str(name)
            c.execute(query) #Execute the que   ry
            conn.commit() #Commit the changes

            flash(f'Post edited for {user}!', 'success')
            return redirect(url_for('Posts'))
        return render_template('edit.html',title='Blog', form=form)    
        
    elif request.method == 'GET':
        form = CarInfoForm()
        c.execute("SELECT Uid,First_name,Last_name FROM User WHERE Uid="+str(currentUser))
        results = c.fetchall()
        users = [(results.index(item), item) for item in results]
        
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("SELECT u.Uid,u.First_name,u.Last_name,p.* FROM Seller s,User u,Post p WHERE p.Uid=s.Uid AND s.Uid=u.Uid AND s.Uid="+str(currentUser)+" AND p.Postid="+name)
        results = c.fetchall()
        # put existing data in column 
        results = results[0]
        # form = CarInfoForm()
        form.username.choices = users
        form.title.data = results[5]
        form.content.data = results[6]
        form.location.data = results[7]
        form.color.data = results[8]
        form.carType.data = results[9]
        form.brand.data = results[10]
        form.price.data = results[11]
        form.manuYear.data = results[12]
        form.image.data = results[16]

        # specialist
        c.execute("SELECT * FROM Specialist")
        specialist_res = c.fetchall()
        specialist = [(specialist_res.index(item), item) for item in specialist_res]
        form.specialist.choices = specialist
        form.stars.choices = ((0,(1)),(1,(2)),(2,(3)))
        form.stars.data = results[15]-1
        form.specialist.data = results[14]-1
        
        return render_template('edit.html',title='Blog', form=form)    
        
# add Post
@app.route("/Posts/new", methods=['GET', 'POST'])
@login_required
def new():
    currentUser=userio.read()
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    #Display all usernames stored in 'users' in the Username field
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    
    # number of post
    c.execute("SELECT COUNT(*) FROM Post")
    postnum = c.fetchall()
    postnum = int(postnum[0][0])+1
    # all user list
    if currentUser>0:
        c.execute("SELECT u.Uid,u.First_name,u.Last_name FROM Seller s,User u WHERE s.Uid=u.Uid AND s.Uid="+str(currentUser))
    else:
        c.execute("SELECT u.Uid,u.First_name,u.Last_name FROM User u, Seller s WHERE u.Uid=s.Uid")
    results = c.fetchall()
    users = [(results.index(item), item) for item in results]
    form = CarInfoForm()
    form.username.choices = users
    # specialist
    c.execute("SELECT * FROM Specialist")
    results = c.fetchall()
    specialist = [(results.index(item), item) for item in results]
    form.specialist.choices = specialist
    form.stars.choices = ((0,(1)),(1,(2)),(2,(3)))
    if form.validate_on_submit():
        choices = form.username.choices
        specialist = form.specialist.choices[form.specialist.data][1]
        stars = form.stars.choices[form.stars.data][1]
        user =  (choices[form.username.data][1])
        title = form.title.data
        content = form.content.data
        location= form.location.data
        color   = form.color.data
        carType =form.carType.data
        brand  = form.brand.data
        price  = form.price.data 
        manuYear = form.manuYear.data
        image = form.image.data
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
        title = title.replace("'","''")
        content = content.replace("'","''")
        #Add the new Post into the 'blogs' table in the database
        query = 'insert into Post (Postid, Date_post, Title,Description,Location,Color,Car_type,Brand,Price,manu_year,Uid,Sid,Stars,Imageid) VALUES (' + "'" + str(postnum) + "',"  + "'" + timestamp + "'," + "'" + title + "',"+ "'" + content + "',"  + "'" + location + "'," + "'" + color + "',"+ "'" + carType + "',"  + "'" + brand + "'," + "'" + price + "'," + "'" + manuYear + "'," + "'" + str(user[0]) + "'," + "'" + str(specialist[0]) + "'," + "'" + str(stars) + "'," + "'" + str(image) + "'" ')' #Build the query
        c.execute(query) #Execute the query
        conn.commit() #Commit the changes

        flash(f'Blog created for {user}!', 'success')
        return redirect(url_for('Posts'))
    return render_template('new.html', title='Blog', form=form)

@app.route("/Posts/<string:name>", methods=['POST'])
def Post_delete(name):
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    query= 'DELETE FROM Post WHERE Postid='+str(name)
    c.execute(query) #Execute the query
    conn.commit() #Commit the changes
    return redirect(url_for('Posts'))

@app.route("/figure", methods=['GET', 'POST'])
def figure():
    if request.method == 'GET':
        title = []
        users = []
        return render_template('figure.html',titles=title,users= users)   
    else:
        title = []
        users = []
        option = request.form.get("special-query")
        conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        if(option == "division"):
            query= 'SELECT b.Uid,u.First_name,u.Last_name  FROM Buyer b, User u WHERE b.Uid=u.Uid AND NOT EXISTS (SELECT i.Inspect_id FROM Inspection i WHERE NOT EXISTS (SELECT bf.Inspect_id FROM Bookfor bf WHERE bf.Inspect_id = i.Inspect_id and bf.Uid = b.Uid))'
            # query = 'SELECT Uid from Buyer'
            c.execute(query) #Execute the query
            rowdata = c.fetchall()
            # lists = [(results.index(item), item) for item in results]
            title = ('Item','User ID','First Name', 'Last Name')
            
        elif(option == "avgprice"):
            # query= 'SELECT AVG(Price) FROM Post WHERE Stars = 1'
            query = 'SELECT AVG(Price), Stars FROM Post GROUP BY Stars'
            # query = 'SELECT Uid from Buyer'
            c.execute(query) #Execute the query
            rowdata = c.fetchall()
            title = ('Item','Average Price ($AU)', 'Stars')
        elif(option == "minwish"):
            query = 'SELECT MIN(p.Price), MAX(p.Price) FROM Post p WHERE p.Postid IN (SELECT DISTINCT(c.Postid) FROM Contain c, Wishlist w WHERE c.Uid = w.Uid AND c.Wishid = w.Wishid AND c.Postid=p.Postid)'
            c.execute(query) #Execute the query
            rowdata = c.fetchall()
            title = ('Item','Minimum Price ($AU)', 'Maximum Price ($AU)')

        num = len(title)
        return render_template('figure.html',titles = title, rows = rowdata,num=num)

#     return redirect(url_for('Posts'))
# return render_template('edit.html',title='Blog', form=form)    
        

if __name__ == '__main__':
    app.run(debug=True)

