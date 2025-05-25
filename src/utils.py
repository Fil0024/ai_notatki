import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def get_root_path():
    this_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(this_file)
    root = os.path.abspath(os.path.join(current_dir, os.pardir))
    return root

def get_pdf_path() -> str:
    """
    Otwiera okno dialogowe do wyboru pliku PDF i zwraca jego ścieżkę.
    """
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    file_path = askopenfilename(
        title="Wybierz plik PDF",
        filetypes=[
            ("Pliki PDF", "*.pdf"),
            ("Wszystkie pliki", "*.*")
        ]
    )
    root.destroy()
    return os.path.abspath(file_path) if file_path else ""

if __name__ == "__main__":
    print("ścieżka źródła" + get_root_path()) 
    
    sciezka = get_pdf_path()
    if sciezka:
        print("Wybrano plik:", sciezka)
    else:
        print("Nie wybrano żadnego pliku.")