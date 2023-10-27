from load_db import load_db as load_db
import panel as pn
import param

class cbfs(param.Parameterized):
    chat_history=param.List([])
    answer=param.String("")
    db_query=param.String("")
    db_response=param.List([])
    
    def __init__(self, **params):
        super(cbfs, self).__init__(**params)
        self.panels=[]
        self.loaded_file="file/dir.pdf"
        self.qa=load_db(self.loaded_file,"stuff",4)
    def call_load_db(self, count):
        if count==0 or file_input.value is None:#init or no file specified
            return pn.pane.Markdown(f"Loaded File: {self.loaded_file}")
        else:
            file_input.save("temp.pdf") #local copy
            self.loaded_file=file_input.file_name
            button_load.button_style="outline"
            self.qa=load_db("temp.pdf", "stuff", 4)
            button_load.button_style="solid"

        self.clr_history()

        return pn.pane.Markdown(f"Loaded File: {self.loaded_file}")
    def convchain(self, query):
        if not query:
            return pn.WidgetBox(pn.Row('User: ', pn.pane.Markdown("", width=600)), scroll=True)
        result=self.qa({"question": query, "chat_history": self.chat_history})
        self.chat_history.extend([query, result["answer"]])
        self.db_query=result["generated_question"]
        self.db_response=result["source_documents"]
        self.answer=result['answer']
        self.panels.extend([
            pn.Row('User:', pn.pane.Markdown(query, width=600)),
            pn.Row('ChatBot:', pn.pane.Markdown(self.answer, width=600, style={"background-color":"#F6F6F6"}))

        ])

        inp.value=''#clears loading indicator when cleared.

        return pn.WidgetBox(*self.panels,scroll=True)
    
