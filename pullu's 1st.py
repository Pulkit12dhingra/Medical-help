from tkinter import *
import sqlite3 
from tkinter import messagebox
import requests as r
import bs4
from PIL import ImageTk, Image
import os
client=sqlite3.connect('D://abc.db')
cu=client.cursor()
try:
    cu.execute("create table login(name varchar(50),age int,password varchar(19),gender varchar(1))")   
    client.commit()
except:
    pass
def login_page():
    global scr,scr1,scr2
    s=0
    try:
        scr1.destroy()
    except:
        pass
    scr=Tk()
    img = ImageTk.PhotoImage(Image.open("D:\pYTHon ProJEct\medical help\login.png"))
    scr.title('Medical_Help Login Page')
    scr.config(bg='White',image=img)
    scr.geometry('800x800')
    
    l1=Label(scr,text="Login OR Sign_up",font=('arial',25,'italic'),bg="Blue",fg="Yellow")
    l1.pack(side=TOP,fill=X)
    l2=Label(scr,text='Username',font=('times',18,'bold'))
    l2.pack()
    e1=Entry(scr,font=('times',16,'italic'))
    e1.pack()
    temp_username=e1.get()
    l3=Label(scr,text="Password",font=('times',18,'bold'))
    l3.pack()
    e2=Entry(scr,font=('times',16,'italic'))
    e2.pack()
    e2.config(show='*')
    def shows():
        e2.config(show='')
    b=Button(scr,text="Show Password",command=shows,bg='Blue',fg='Red')
    b.pack()
    def register():
        signup_page()        
    b1=Button(scr,text='Sign_up',command=register,bg='Green',fg='Black')
    b1.pack()
    def login():
        cu.execute("select count(*) from login where name=%r and password=%r"%(e1.get(),e2.get()))
        a=cu.fetchall()
        if a[0][0]==1:
            main_page()
        else:
            messagebox.showerror("Login Failed","Username or password incorrect")
    b2=Button(scr,text='Log_in',command=login,bg='Red',fg='Purple')
    b2.pack()
    scr.mainloop()
def signup_page():
    global scr1
    var=DoubleVar()
    scr.destroy()
    temp=""
    scr1=Tk()
    scr1.geometry('800x800')
    scr1.title('Sign Up !!')
    scr1.geometry('800x800')
    l1=Label(scr1,text="Register Yourself :)",font=('arial',25,'italic'),cursor='heart',bg="blue",fg="Red")
    l1.pack(side=TOP,fill=X)
    l2=Label(scr1,text="UserName :",font=('arial',18,'bold'))
    l2.pack()
    e1=Entry(scr1,font=('arial',18,'bold'))
    e1.pack()
    l3=Label(scr1,text="Age :",font=('arial',18,'bold'))
    l3.pack()
    e2=Entry(scr1,font=('arial',18,'bold'))
    e2.pack()
    l4=Label(scr1,text="Gender :",font=('arial',18,'bold'))
    l4.pack()
    def funn():
        if var.get()==0.0:
            return("Male")
        if var.get()==1.0:
            return("Female")
    r1=Radiobutton(scr1,text='Male',command=funn,variable=var,value=0.0)
    r1.pack()
    r2=Radiobutton(scr1,text='Female',command=funn,variable=var,value=1.0)
    r2.pack()
    temp=funn()
    l5=Label(scr1,text="Password :",font=('arial',18,'bold'))
    l5.pack()
    e3=Entry(scr1,font=('arial',18,'bold'))
    e3.pack()
    def fnd():
        cu.execute("insert into login values('{}',{},'{}','{}')".format(e1.get(),int(e2.get()),e3.get(),temp))
        client.commit()
        messagebox.showinfo("Registration","Registration Successful")
        login_page()
    b4=Button(scr1,text='Submit',command=fnd)
    b4.pack()
    scr1.mainloop()
def main_page():
    scr.destroy()
    scr2=Tk()
    scr2.geometry('800x800')
    l1=Label(scr2,text="Main Page",font=('arial',25,'italic'),bg='Yellow',fg='Red')
    l1.pack(side=TOP,fill=X)
    l2=Label(scr2,text="Enter any medicie name and search it's details",font=('arial',18,'italic'),fg='Blue')
    l2.pack()
    e1=Entry(scr2,font=('times',16,'italic'))
    e1.pack()
    global m 
    m=Message(scr2,bg='yellow')
    def scrap():
        lst=[]
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        dt=r.request('get','https://www.1mg.com/search/all?name=%s'%(e1.get()))
        s=bs4.BeautifulSoup(dt.text,'html.parser')
        for i in s.findAll('div'):
            if i.get('class'):
                if len([x for x in i.get('class') if 'style__container__' in x])>0:
                    if i.find('a'):
                        x=i.find('a')
                        try:
                    
                            dts=r.request('get','https://www.1mg.com'+x.get('href'),headers={'User-Agent': user_agent})
                            s1=bs4.BeautifulSoup(dts.text,'html.parser')
                            for j in s1.findAll('div'):
                                if j.get('class'):
                                    if len([x for x in j.get('class') if '_product-description' in x])>0:
                                    
                                        try:
                                            lst.append(j.text)    
                                        except:
                                            pass
                                        
                                    elif  len([x for x in j.get('class') if 'DrugOverview__container' in x])>0:
                                    
                                        try:
                                            lst.append(j.text)
                                        except:
                                            pass
                        except:
                            pass

        global data,m                    
        data=iter(lst)
        try:
            m.config(text=next(data))
        except:
            pass
    b1=Button(scr2,text='Search',font=('times',16,'bold'),bg='green',fg='white',command=scrap)
    b1.pack()
    def nexxt():
        global m,data
        try:
            m.config(text=next(data))
        except:
            m.config(text="Finish ,   thanks for search    !!!",width=210)
   
    m.pack()
    b2=Button(scr2,text='Next',font=('times',16,'bold'),command=nexxt)    
    b2.pack(side=BOTTOM)        
    scr2.mainloop()
login_page()


    
