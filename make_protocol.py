import docx

doc = docx.Document('official_protocol.docx')
dictionary = {
    "совещания": "coвещания",
    "регион": "регион",
    "ДАТА": "dd.mm.yyyy",
    "номер1": "номер",
    "список участников": ("должность - ФИО", "должность - ФИО"),
    "тема совещания": "тема совещания",
    "участники1": ("ФИО1", "ФИО2"),
    "доклады": (["Цель обсуждения", "Контекст обсуждения: контекст", "Время : 00:00-00:00"],
                ["Цель обсуждения", "Контекст обсуждения: контекст", "Время : 00:00-00:00"]),
    "номер2": "номер",
    "ТЕМА": "ТЕМА",
    "список поручений": (["АДРЕСАТ ПОРУЧЕНИЯ", "ЗАДАЧА", "СРОК"], ["АДРЕСАТ ПОРУЧЕНИЯ", "ЗАДАЧА", "СРОК"])
}

for i in dictionary:
    for p in doc.paragraphs:
        if i in p.text:
            if isinstance(dictionary[i], str):
                p.text = p.text.replace(i, dictionary[i])
            elif isinstance(dictionary[i][0], list):
                d = []
                for j in range(0, len(dictionary[i])):
                    dictionary[i][j][0] = str(j + 1) + '. ' + dictionary[i][j][0]
                    new_text = '\n'.join(dictionary[i][j])
                    d.append(new_text)
                new_text = '\n''\n'.join(d)
                p.text = p.text.replace(i, new_text)
            else:
                new_text = '\n'.join(dictionary[i])
                p.text = p.text.replace(i, new_text)
doc.save('official_protocol.docx')