from uiComponents import App

def main():
    app = App()
    # frame = ScrollableFrame(app)
    # frame.pack(fill='both', expand=True)

    app.runApp(title="Crowell's Files Reviewer",
               size="500x300")
    
if __name__ == "__main__":
    main()
