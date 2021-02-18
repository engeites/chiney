from misc.separate import tokenize


class Handler():
    mystery_char = f"{chr(10)}{chr(13)}"

    def __init__(self, data):
        self.post = data
        print(type(data))
        print(data.translation)

    def handle_text(self, data):
        print('STARTING DIVISION')

        paragraphs = self.post.text.replace(self.mystery_char, '\n\n').split('\n\n')
        print(f"SPLIT INTO {len(paragraphs)} PARAGRAPHS!")
        return paragraphs

    def do_tokenize(self, data):
        paragraphs = self.handle_text(data)
        print("STARTING TOKENIZING")
        tokens = []
        length = len(paragraphs)
        for par in paragraphs:
            tokenized_text = tokenize(par)
            tokens.append(list(tokenized_text))
        print("FINISHED TOKENIZING")
        return tokens

    def gather_and_send(self):
        tokens = self.do_tokenize(self.post.text)
        bunch = {
            'tokens': tokens,
            'tran_pars': self.handle_text(self.post.translation),
            'header': self.post.header,
            'description': self.post.description,
            'author': self.post.author,
            'level': self.post.level,
            'date': self.post.date
        }
        return bunch
