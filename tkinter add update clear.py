from tkinter import*
from tkinter import ttk





class student:
    def __init__(self,main):
        self.main=main
        self.T_Frame=Frame(self.main,height=50,width=1200,background='magenta',bd=2,relief=GROOVE)
        self.T_Frame.pack()
        self.Title=Label(self.T_Frame, text='student mangement system',font='ariel 20 bold',width=1200,bg='magenta')
        self.Title.pack()

        self.Frame_1=Frame(self.main,height=580,width=400,bd=2,relief=GROOVE,bg='red')
        self.Frame_1.pack(side=LEFT)
        self.Frame_1.pack_propagate(0)

        Label(self.Frame_1,text='student detials',background='orange',font='arial 12 bold').place(x=20,y=20)
        self.Id=Label(self.Frame_1,text='Id',background='yellow',font='arial 11 bold')
        self.Id.place(x=40,y=60)
        self.Id_Entry=Entry(self.Frame_1,width=40)
        self.Id_Entry.place(x=150,y=60)

    
        self.name=Label(self.Frame_1,text='name',background='yellow',font='arial 11 bold')
        self.name.place(x=40,y=100)
        self.name_Entry=Entry(self.Frame_1,width=40)
        self.name_Entry.place(x=150,y=100)

        self.age=Label(self.Frame_1,text='age',background='yellow',font='arial 11 bold')
        self.age.place(x=40,y=140)
        self.age_Entry=Entry(self.Frame_1,width=40)
        self.age_Entry.place(x=150,y=140)

        self.DOP=Label(self.Frame_1,text='DOP',background='yellow',font='arial 11 bold')
        self.DOP.place(x=40,y=180)
        self.DOP_Entry=Entry(self.Frame_1,width=40)
        self.DOP_Entry.place(x=150,y=180)

        self.Gender=Label(self.Frame_1,text='Gender',background='yellow',font='arial 11 bold')
        self.Gender.place(x=40,y=220)
        self.Gender_Entry=Entry(self.Frame_1,width=40)
        self.Gender_Entry.place(x=150,y=220)

        self.mark=Label(self.Frame_1,text='mark',background='yellow',font='arial 11 bold')
        self.mark.place(x=40,y=260)
        self.mark_Entry=Entry(self.Frame_1,width=40)
        self.mark_Entry.place(x=150,y=260)

        self.Button_Frame=Frame(self.Frame_1,height=250,width=250,relief=GROOVE,bd=2,background='green')
        self.Button_Frame.place(x=80,y=300)

    
        self.Add=Button(self.Button_Frame,text='Add',width=25,font='arial 11 bold',background='blue',command=self.Add)
        self.Add.pack()

        self.Delete=Button(self.Button_Frame,text='Delete',width=25,font='arial 11 bold',background='grey',command=self.Delete)
        self.Delete.pack()

        self.update=Button(self.Button_Frame,text='update',width=25,font='arial 11 bold',background='orange',command=self.update)
        self.update.pack()

        self.clear=Button(self.Button_Frame,text='clear',width=25,font='arial 11 bold',background='cyan',command=self.clear)
        self.clear.pack()



        self.Frame_2=Frame(self.main,height=580,width=800,bd=2,relief=GROOVE,bg='green')
        self.Frame_2.pack(side=RIGHT)

        self.tree=ttk.Treeview(self.Frame_2,columns=('c1','c2','c3','c4','c5','c6'),show='headings',height=25)
        self.tree.column('#1',anchor=CENTER,width=95)
        self.tree.heading('#1',text='ID')

        self.tree.column('#2',anchor=CENTER,width=100)
        self.tree.heading('#2',text='name')

        self.tree.column('#3',anchor=CENTER,width=105)
        self.tree.heading('#3',text='Age')

        self.tree.column('#4',anchor=CENTER,width=110)
        self.tree.heading('#4',text='DOB')

        self.tree.column('#5',anchor=CENTER,width=115)
        self.tree.heading('#5',text='Gender')

        self.tree.column('#6',anchor=CENTER,width=120)
        self.tree.heading('#6',text='Mark')
        self.tree.pack()

        self.tree.insert("",index=0,values=(1,"A.Aravind",29,"11-9-95","male",85))
        self.tree.pack()

    def Add(self,):
        id=self.Id_Entry.get()
        name=self.name_Entry.get()
        age=self.age_Entry.get()
        dob=self.DOP_Entry.get()
        gender=self.Gender_Entry.get()
        mark=self.mark_Entry.get()

        self.tree.insert("",index=0,values=(id,name,age,dob,gender,mark))

        
    def Delete(self):
        item=self.tree.selection()[0]
        self.tree.delete(item)

    def update(self,):
        id=self.Id_Entry.get()
        name=self.name_Entry.get()
        age=self.age_Entry.get()
        dob=self.DOP_Entry.get()
        gender=self.Gender_Entry.get()
        mark=self.mark_Entry.get()
        item=self.tree.selection()[0]
        self.tree.item(item,values=(id,name,age,dob,gender,mark))
    def clear(self):
        self.Id_Entry.delete(0,END)
        self.name_Entry.delete(0,END)              
        self.age_Entry.delete(0,END)
        self.DOP_Entry.delete(0,END)
        self.Gender_Entry.delete(0,END)
        self.mark_Entry.delete(0,END)
            

       
    
    
        
                     

        

main=Tk()
main.title('student mangement system')
main.geometry('600x400')

student(main)
main.mainloop()
        

  
