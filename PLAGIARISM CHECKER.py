from tkinter import *
from tkinter import filedialog
import tkinter.font as fnt
import numpy as np
import glob
import os


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1

    # defining a zero matrix of size of first string * second string
    matrix = np.zeros((size_x, size_y))

    for x in range(size_x):
        matrix[x, 0] = x  # row aray with elements of x
    for y in range(size_y):
        matrix[0, y] = y  # column array with elements of y
    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:  # if the alphabets at the postion is same
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )

            else:  # if the alphabbets at the position are different
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )

    # returning the levenshtein distance i.e last element of the matrix
    return (matrix[size_x - 1, size_y - 1])


window = Tk()
width= window.winfo_screenwidth()
height= window.winfo_screenheight()
window.title("Plagiarism Checker")
window.geometry("%dx%d" % (1280,780))
window.resizable(True, True)

def MasterWithFolder():
    master = Toplevel(window)
    master.title("Comparing folder with Masterfile")
    master.geometry("700x500")

    def folderVsMaster(plag):
        plag = float(plag)
        global FolderPath
        path1 = FolderPath
        os.chdir(path1)
        # opening all text files within the folder and stores them in an array
        myFiles = glob.glob('*.txt')

        wrapper2 = LabelFrame(master, text="Output")
        wrapper2.pack(fill=X, padx=10, pady=10)

        Label1 = Label(wrapper2, text="The text files available are :").grid(row=4, column=0)
        Label2 = Label(wrapper2, text=myFiles).grid(row=4, column=1)

        global FilePath
        path = FilePath
        with open(path, 'r', encoding="utf8") as file:
            data = file.read().replace('\n', '')
            str1 = data.replace(' ', '')


        for i in range(0, len(myFiles)):
            with open(myFiles[i], 'r', encoding="utf8") as file:
                data = file.read().replace('\n', '')
                str2 = data.replace(' ', '')
            if (len(str1) > len(str2)):
                length = len(str1)
            else:
                length = len(str2)

            n = 100 - round((levenshtein(str1, str2) / length) * 100, 2)

            if (n > plag):
                Label3 = Label(wrapper2, text="Plagiarised files are :").grid(row=6, column=0)
                Label4 = Label(wrapper2, text=[path, "and", myFiles[i]," are ", n, "% plagiarised"]).grid(row=i + 6, column=1)
            else:
                Label5 = Label(wrapper2, text = ["Similarities are below the given level for ", myFiles[i], "and", path]).grid(row=i+6, column=1)



    FolderPath = "StringVar()"
    FilePath = "StringVar()"

    def open_folder():
        global FolderPath
        folderpath = filedialog.askdirectory()
        FolderPath = folderpath
        print(FolderPath)

    def open_masterfile():
        global FilePath
        filepath = filedialog.askopenfilename()
        FilePath = filepath
        print(FilePath)

    wrapper1 = LabelFrame(master, text="Input")
    wrapper1.pack(fill=X, padx=10, pady=10)

    Percentage = IntVar()
    percentLabel = Label(wrapper1, text="Enter the percent of plagiarism allowed: ").grid(row=0, column=0, padx=10, pady=10)
    Percent = Entry(wrapper1, textvariable=Percentage).grid(row=0, column=1)
 
    folderLabel = Label(wrapper1, text="Open the complete folder containing all files to compare: ").grid(row=1, column=0, padx=10, pady=10)
    folder1 = Button(wrapper1, text="Browse", textvariable=FolderPath, command=open_folder).grid(row=1, column=1)

    MasterLabel = Label(wrapper1, text="Open the Master file from which you want to compare: ").grid(row=2, column=0, padx=10, pady=10)
    file2 = Button(wrapper1, text="Browse", textvariable=FilePath, command=open_masterfile).grid(row=2, column=1)

    B_Submit = Button(wrapper1, text="Submit", command=lambda: folderVsMaster(Percentage.get()))
    B_Submit.grid(row=3, column=0, padx=10, pady=10)


def Two_Files():
    twoFiles = Toplevel(window)
    twoFiles.title("Check for plagiarism in two files")
    twoFiles.geometry("855x480")

    def PlagInTwoFile(plag):
        wrapper2 = LabelFrame(twoFiles, text="Output")
        wrapper2.pack(fill=X, padx=10, pady=10)
        plag = float(plag)
        global FirstPath
        global SecondPath
        path2 = FirstPath
        path3 = SecondPath
        with open(path2, 'r', encoding="utf8") as file:
            data = file.read().replace('\n', '')
            str1 = data.replace(' ', '')

        with open(path3, 'r', encoding="utf8") as file:
            data = file.read().replace('\n', '')
            str2 = data.replace(' ', '')

        if (len(str1) > len(str2)):
            length = len(str1)

        else:
            length = len(str2)

        n = 100 - round((levenshtein(str1, str2) / length) * 100, 2)

        if (n > plag):
            Label1 = Label(wrapper2, text="Both files have ").pack(side=LEFT)
            Label2 = Label(wrapper2, text=n).pack(side=LEFT)
            Label3 = Label(wrapper2, text=" % Plagiarism").pack(side=LEFT)
        else:
            Label2 = Label(wrapper2, text="Similarities are below the given level.").pack(side=LEFT, padx=10, pady=10)

    Percentage = IntVar()
    FirstPath = "StringVar()"
    SecondPath = "StringVar()"

    def open_file1():
        global FirstPath
        filepath = filedialog.askopenfilename()
        FirstPath=filepath
        print(filepath)
    def open_file2():
        global SecondPath
        filepath = filedialog.askopenfilename()
        SecondPath=filepath
        print(filepath)

    wrapper1 = LabelFrame(twoFiles, text="Input")
    wrapper1.pack(fill=X, padx=10, pady=10)

    percentLabel = Label(wrapper1, text="Enter the percent of plagiarism allowed: ").grid(row=0, column=0, padx=10, pady=10)
    Percent = Entry(wrapper1, textvariable=Percentage).grid(row=0, column=1)

    file1Label = Label(wrapper1, text="Open the first file to compare: ").grid(row=1, column=0, padx=10, pady=10)
    file1 = Button(wrapper1, text="Browse",textvariable=FirstPath, command=open_file1).grid(row=1, column=1)

    file2Label = Label(wrapper1, text="Open the second file to compare: ").grid(row=2, column=0, padx=10, pady=10)
    file2 = Button(wrapper1, text="Browse",textvariable=SecondPath, command=open_file2).grid(row=2, column=1)

    B_Submit = Button(wrapper1, text="Submit",command=lambda: PlagInTwoFile(Percentage.get()))
    B_Submit.grid(row=3, column=0, padx=10, pady=10)


def Folder_Files():
    folderCheck = Toplevel(window)
    folderCheck.title("Check for plagiarism in all files in folder")
    folderCheck.geometry("900x700")

    def PlagInFolder(plag):
        plag = float(plag)
        print(plag)
        global FolderPath
        path1 = FolderPath
        os.chdir(path1)

        wrapper2 = LabelFrame(folderCheck, text="Output")
        wrapper2.pack(fill=X, padx=10, pady=10)

        # opening all text files within the folder and stores them in an array
        myFiles = glob.glob('*.txt')
        Label1 = Label(wrapper2, text="The text files available are :").grid(row=3, column=0)
        Label2 = Label(wrapper2, text=myFiles).grid(row=3, column=1)


        for i in range(0, len(myFiles)):
            for j in range(i, len(myFiles)):

                with open(myFiles[i], 'r', encoding="utf8") as file:
                    data = file.read().replace('\n', '')
                    str1 = data.replace(' ', '')

                with open(myFiles[j], 'r', encoding="utf8") as file:
                    data = file.read().replace('\n', '')
                    str2 = data.replace(' ', '')

                if (len(str1) > len(str2)):
                    length = len(str1)
                else:
                    length = len(str2)
                if (myFiles[i] != myFiles[j]):

                    n = 100 - round((levenshtein(str1, str2) / length) * 100, 2)
                    if (n > plag):
                        Label3 = Label(wrapper2, text="Plagiarised files are :").grid(row=4, column=0)
                        Label4 = Label(wrapper2, text=[myFiles[i], "and", myFiles[j], n, "% plagiarised"]).grid(column=1)
                    else:
                        Label2 = Label(wrapper2, text=["Similarities are below the given level for ",myFiles[i], "and", myFiles[j]]).grid(column=1)

    Percentage = IntVar()
    FolderPath = "StringVar()"
    def open_folder():
        global FolderPath
        folderpath = filedialog.askdirectory()
        FolderPath=folderpath
        print(folderpath)

    wrapper1 = LabelFrame(folderCheck, text="Input")
    wrapper1.pack(fill=X, padx=10, pady=10)

    percentLabel = Label(wrapper1, text="Enter the percent of plagiarism allowed: ").pack(side=LEFT, padx=10, pady=10)
    Percent = Entry(wrapper1, textvariable=Percentage).pack(side=LEFT, padx=10, pady=10)  #.grid(row=0, column=1)

    folderLabel = Label(wrapper1, text="Open the complete folder containing all files to compare: ").pack(side=LEFT, padx=10, pady=10)  #.grid(row=1,column=0)
    folder = Button(wrapper1, text="Browse", textvariable=FolderPath, command=open_folder).pack(side=LEFT, padx=10, pady=10) #.grid(row=1, column=1)

    B_Submit = Button(wrapper1, text="Submit",command=lambda: PlagInFolder(Percentage.get())).pack(padx=10, pady=10)  #.grid(row=2, column=0)

wrapper = LabelFrame(window)
wrapper.pack(fill="both", expand="yes", padx=10, pady=10)
photo = PhotoImage(file="checker bg.png")
WelScreen = Label(wrapper, image=photo).pack()
Button1 = Button(wrapper, text="Comparing folder with Masterfile", activebackground="grey", command=MasterWithFolder,
                 font=fnt.Font(size = 15), width=50, height=2)
Button2 = Button(wrapper, text="Check for plagiarism in Two Files", activebackground="grey", command=Two_Files,
                 font=fnt.Font(size = 15), width=50, height=2)
Button3 = Button(wrapper, text="Check for plagiarism in all Files in Folder", activebackground="grey", command=Folder_Files,
                 font=fnt.Font(size = 15), width=50, height=2)
Button1.place(x=370, y=400)
Button2.place(x=370, y=470)
Button3.place(x=370, y=540)

window.mainloop()