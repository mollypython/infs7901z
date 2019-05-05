from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RatingForm, WishlistForm, InspectionForm
from flaskblog.models import User
import mysql.connector

#rating
@app.route("/rating", methods=['GET', 'POST'])
def rating():
    if request.method == 'GET':
        conn = mysql.connector.connect(user='root',password='root', database='infs7901')
        #conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Rating")
        rating = cursor.fetchall()

    return render_template('rating.html', title='Rating', rform=rform)


def add_rating():
    form = RatingForm()
    if form.validate_on_submit():
        conn = mysql.connector.connect(user='root',password='root', database='infs7901')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Rating VALUES' )
        conn.commit()
        flash(f'New Rating{rform.Rid.data}has been created.', 'success')
        return redirect(url_for('home'))
    return render_template('rating.html', title='Rating', rform=rform)

def delete_rating():
    conn = mysql.connector.connect(user='root',password='root', database='infs7901')
    conn.row_factory = lambda cursor, row: row[0]
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Rating WHERE Postid='+str(name))
    flash(f'Rating{rform.Rid.data}has been deleted.', 'success') 
    conn.commit() 
    return redirect(url_for('rating'))
  

   
@app.route("/wishlist", methods=['GET', 'POST'])
def wishlist():
    if request.method == 'POST':
        conn = mysql.connector.connect(user='root',password='root', database='infs7901')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Wishlist","SELECT Postid FROM Post.P, Wishlist.W WHERE P.Uid = W.Uid")
        wishlist = cursor.fetchall()

        return render_template('wishlist.html', title='Wishlist', wform=wform)
    
    else:
        conn = mysql.connector.connect(user='root',password='root', database='infs7901')
        uid = (request.form.get("Uid"))
        wishid = (request.form.get("Wishid"))
        postid = (request.form.get("Postid"))

        cond = 'WHERE'
        count = 0
        if uid is not None:
            count = count + 1
            cond = cond + "Uid LIKE '%' + uid + '%'"
        if wishid is not None:
            if count>0:
                cond += ' AND '
            count = count + 1
            cond = cond + "Wishid LIKE '%' + wishid + '%'"
        if postid is not None:
            if count > 0:
                cond += " AND "
            count = count + 1
            cond = cond + "Postid LIKE '%' + postid + '%'"
            
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Wishlist" + cond)
        wishlist = cursor.fetchall()
        return render_template('wishlist.html', title='Wishlist', wform=wform)
    
def add_wishlist():
    form = WishlistForm()
    if form.validate_on_submit():
       conn = mysql.connector.connect(user='root',password='root', database='7901')
       cursor = conn.cursor()
       cursor.execute('INSERT INTO Wishlist(wishid, uid) VALUES(%s, %s)',['6', '6'])
       conn.commit()        
       flash(f'New Wishlist {form.wishid.data}!', 'success')
    return render_template('wishlist.html', title='Wishlist', wform=wform)

def delete_wishlist():
    conn = mysql.connector.connect(user='root',password='root', database='infs7901')
    conn.row_factory = lambda cursor, row: row[0]
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Wishlist WHERE wishid='+str())
    flash(f' Wish{rform.Wishid.data}has been deleted.', 'success') 
    conn.commit() 
    return redirect(url_for('wishlist'))

#Add Blog
@app.route("/inspection", methods=['GET', 'POST'])
def inspection():
    if request.method == 'GET':
        conn = mysql.connector.connect(user='root',password='root', database='7901')
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Inspection")
        wishlist = cursor.fetchall()

        return render_template('inspection.html', title='Inspection', iform=iform)
    
    else:
        conn = mysql.connector.connect(user='root',password='root', database='7901')
        inspect_id = (request.form.get("inspect_id"))
        location = (request.form.get("location"))
        if_booked = (request.form.get("if_booked"))
        postid = (request.form.get("postid"))

        cond = 'WHERE'
        count = 0
        if inspect_id is not None:
            count = count + 1
            cond = cond + "Inspect_id LIKE '%' + inspect_id + '%'"
        if location is not None:
            if count>0:
                cond += ' AND '
            count = count + 1
            cond = cond + "Location LIKE '%' + location + '%'"
        if if_booked is not None:
            if count>0:
                cond += ' AND '
            count = count + 1
            cond = cond + "If_booked LIKE '%' + if_booked + '%'"     
        if postid is not None:
            if count > 0:
                cond += " AND "
            count = count + 1
            cond = cond + "Postid LIKE '%' + postid + '%'"
            
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Inspection" + cond)
        inspection = cursor.fetchall()
        return render_template('inspection.html', title='Inspection', iform=iform)
    
def add_inspection():
    form = InspectionForm()
    if form.validate_on_submit():
        conn = mysql.connector.connect(user='root',password='root', database='7901')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Inspection VALUES)
        conn.commit()
        flash(f'This is your inspection!', 'success')
    return render_template('Inspection.html', title='Inspection', iform=iform)

def delete_inspection():
    conn = mysql.connector.connect(user='root',password='root', database='infs7901')
    conn.row_factory = lambda cursor, row: row[0]
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Inspection WHERE inspect_id='+str())
    flash(f' Inspection{rform.inspect_id.data}has been deleted.', 'success') 
    conn.commit() 
    return redirect(url_for('inspection'))
