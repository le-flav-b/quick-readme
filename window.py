from preview_window import tk, PreviewWindow

class Window:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1080x720')
        self.root.iconbitmap('icon.ico')
        self.root.title("Quick Readme")
        self.darkmode = True
        self.sections = [line.split(' : ') + [None] for line in open('sections.txt', 'r').read().split('\n')]
        self.root.mainloop()
    
    def change_mode(self):
        self.darkmode = not self.darkmode

    def preview(self):
        PreviewWindow(self.darkmode, self.sections)
