import jagger
import tkinter as tk
from tkinter import filedialog
from jamdict import Jamdict
from createFlashCards import createDeck

words = []

particles = [
  "は", "が", "を", "に", "へ", "と", "で", "から", "まで",
  "より", "の", "も", "や", "など", "か", "ね", "よ", "ぞ", "ぜ", "さ", "な", "わ"
]
polite_endings = ["ます", "ました", "ません", "ませんでした"]
plain_endings = ["る", "た", "ない", "なかった", "たかった", "たくない"]
te_form = ["て", "で", "てる", "ている", "でいる", "ていない", "でいない", "ちゃう", "じゃう"]
past_forms = ["た", "だ", "たんだ", "だった"]
potential_forms = ["れる", "られる", "できる"]
causative_forms = ["せる", "させる"]
passive_forms = ["れる", "られる"]
volitional_forms = ["よう", "ましょう"]
conditional_forms = ["ば", "たら", "なら"]
imperative_forms = ["ろ", "れ", "なさい"]
copula = ["です", "だ", "だった", "じゃない", "ではない"]
conjunctions = ["ので"]

exclusions_set = {
    "は", "が", "を", "に", "へ", "と", "で", "から", "まで", "より", "の", "も", "や", "など",
    "か", "ね", "よ", "ぞ", "ぜ", "さ", "な", "わ", "ます", "ました", "ません", "ませんでした",
    "る", "た", "ない", "なかった", "たかった", "たくない", "て", "で", "てる", "ている",
    "でいる", "ていない", "でいない", "ちゃう", "じゃう", "た", "だ", "たんだ", "だった",
    "れる", "られる", "できる", "せる", "させる", "よう", "ましょう", "ば", "たら", "なら",
    "ろ", "れ", "なさい", "です", "だ", "だった", "じゃない", "ではない", "いる", "ので"
}

def is_word(token):
    return token in exclusions_set



jam = Jamdict(db_mode=":memory:")

model_path = "model/kwdlc/patterns"
tokenizer = jagger.Jagger()
tokenizer.load_model(model_path)

root = tk.Tk()

root.geometry("500x500")
root.title("BookTokenizer")

label = tk.Label(root, text="Tokenize Book", font=('Arial', 18))
label.pack(padx=20, pady=20)

textbox = tk.Text(root, height=3, font=('Arial', 16))
textbox.pack(padx=10)


def UploadAction(event=None):
    filename = filedialog.askopenfile()
    print('Selected:', filename)

def TokenizeText(event=None):
    japaneseText = textbox.get("1.0",'end-1c')
    toks = tokenizer.tokenize(japaneseText)
    for tok in toks:
        if is_word(tok.surface()):
            print("-")
        elif(tok.surface().isalpha()):
            print("+")
            # print(f"'{tok.surface()}' is a word")
            words.append(jam.lookup(tok.feature().split(",")[4]))
            # words(jam.lookup(tok.feature().split(",")[4]))
            # print(jam_word.entries[0].senses)
        print("|")
    print("EOS")
    createDeck(wordList=words)

button = tk.Button(root, text="Open", command=TokenizeText, font=('Arial', 18))
button.pack(padx=20)


root.mainloop()
