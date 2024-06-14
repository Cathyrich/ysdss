import openai_intr

if __name__ == '__main__':
    history = openai_intr.premise_history

    print(history)

    file_path = '/Users/wei/Downloads/优秀案例材料.docx'
    info = openai_intr.file_upload(file_path,
                            "我写了一篇文章，请结合《国企》这本杂志的文章风格，帮我润色文章，并小幅度的拓展字数",
                            history)
    print(info[0].content)