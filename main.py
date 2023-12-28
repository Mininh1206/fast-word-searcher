from tkinter import *
from tkinter import filedialog
import os
from PyPDF2 import PdfReader

window = Tk()
entryWord = StringVar()
selectedDirectory = StringVar()
filesList = Listbox(window, bg="gray")

def defineWindow():
    window.title("Buscador de palabras")
    window.geometry("700x300")
    window.iconbitmap("favicon.ico")
    window.resizable(0, 0)

    sideFrame = Frame(window)

    selectDirectoryFrame = Frame(sideFrame)

    selectDirectoryButton = Button(selectDirectoryFrame, text="Seleccionar carpeta", command=selectDirectory, width=16)
    selectDirectoryButton.pack(side="left", padx=5, pady=10)

    selectDirectoryLabel = Label(selectDirectoryFrame, textvariable=selectedDirectory)
    selectedDirectory.set("Selecciona un directorio...")
    selectDirectoryLabel.pack(side="left", fill="x", expand=True)

    selectDirectoryFrame.pack(side="top", fill="x")

    wordFrame = Frame(sideFrame)

    searchButton = Button(wordFrame, text="Buscar", command=searchInDirectory, width=16)
    searchButton.pack(side="left", padx=5, pady=10)

    wordInput = Entry(wordFrame, textvariable=entryWord)
    wordInput.pack(side="left", fill="x", expand=True)

    wordFrame.pack(side="top", fill="x")

    sideFrame.pack(side="left", fill="y", padx=10, pady=10)
    filesList.pack(side="left", expand=True, fill="both")

    filesList.bind("<Double-Button-1>", openFile)

    window.mainloop()

def openFile(evt):
    indexSelectedFile = filesList.curselection()[0]
    selectedFile = str(filesList.get(indexSelectedFile))

    if selectedFile != None and selectedFile != "":
        os.system(f"\"{selectedFile}\"")

def selectDirectory():
    newSelectedDirectory = str(filedialog.askdirectory())

    if newSelectedDirectory != None and newSelectedDirectory != "":
        selectedDirectory.set(newSelectedDirectory)

def searchInDirectory():
    if selectedDirectory.get() != None and selectedDirectory.get() != "" and entryWord.get() != None and entryWord.get() != "":
        filesList.delete(0, END)

        directory = str(selectedDirectory.get())
        
        searchFiles(directory)

def searchFiles(directory: str):
    filesInDirectory = os.listdir(directory)

    for f in filesInDirectory:
        newRoute = str(directory + "/" + f)

        if os.path.isdir(newRoute):
            searchFiles(newRoute)
        else:
            searchWord(newRoute)

def searchWord(route: str):
    f = open(route, "rb")

    try:
        if not route.endswith(".pdf"):
            for b in f:
                try:
                    line = b.decode('UTF-8')
                    if entryWord.get() in line:
                        filesList.insert(0, route)
                        break
                except Exception:
                    pass
        else:
            pdfReader = PdfReader(f)
            
            for page in pdfReader.pages:
                if entryWord.get() in page.extract_text():
                    filesList.insert(0, route)
                    break
    except Exception:
        pass

    f.close()

    
    

if __name__ == "__main__":
    defineWindow()