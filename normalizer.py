import os
import re
import corpus_utils
from hazm import Normalizer


punctuations = ["!", "\"", "(", ")", "?", "*", ",", "-","/", ":", "[", "]", "«", "»", "،", "؛", "؟", "+",
                 "…","$", "|", "{", "}", "٫", ";", ">", "<", "@", "\\", ".", "&", "'" ,"‧" ,"″", "‹", "›", "※", "‼", "⁉"]
punct_str = "،!\"()?*,-./:[]«» +-…$|{}٫;><@&'‧″‹›※‼⁉\\"
digits = "۰۱۳۲۴۵۶۷۸۹"
whitespace_chars = "\t\x0b\x0c\r\x1c\x1d\x1e\x1f \x85\xa0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000\u180e\u200b\u200c\u200d\u2060\ufeff"

normalizer = None
incorrect = None
correct = None

def loadCodings(TableCodingsFile):
    # Open the file containing the codings and remove '\ufeff' character.
    with open(TableCodingsFile, encoding="UTF-8") as f:
        content = f.read().split("\n")
        list_content = list(content)[1:]
        codings = [i.split("\t") for i in list_content]
    inc = [i[0] for i in codings]
    c = [i[1] for i in codings]
    return inc, c


def CorrectCodingInLine(line, incorrect, correct):
    # Correct the codings.
    normalized_line = ""
    for i in range(len(line)):
        if line[i] in incorrect:
            ind = incorrect.index(line[i])
            normalized_line += correct[ind]
        else:
            normalized_line += line[i]
    return normalized_line


def CorrectCodingInFile(Path, InTextFilename, TableCodingsFile):
    ''' Returns the text with correct, unified coding.
    Input: InTextFilename(str), TableCodings(str)
    Output: normalized_text (str)
    '''
    incorrect, correct = loadCodings(TableCodingsFile)
    #Open the file to be corrected.
    for line in open(Path+InTextFilename, encoding="UTF-8"):
        normalized_line = CorrectCodingInLine(line, incorrect, correct)
        #Write the result to a file.
        with open(Path + "CorpusAllCodings.txt", "a+", encoding = "UTF8") as g:
            g.write(normalized_line)

    return

def prepare_line(line):
    global normalizer, incorrect, correct, unicode_redundant_chars, whitespace_chars, digits, punct_str, punctuations
    if normalizer is None:
        normalizer = Normalizer()
        incorrect, correct = loadCodings("TableCodings.txt")

    line = normalizer.normalize(line)
    line = CorrectCodingInLine(line, incorrect, correct)

    pat = re.compile(r"([" + re.escape(punct_str) + "])")
    line = re.sub(pat, r" \1 ", line)

    pat = re.compile(r"([" + digits + "]+)")
    line = re.sub(pat, r" \1 ", line)
    pat = re.compile(r"\n+")
    line = re.sub(pat, r" \n ", line)
    pat = re.compile("[" + whitespace_chars + "]+")
    line = re.sub(pat, r" ", line)
    line = line.strip()
    return line

def normalize_instagram_file(in_path, out_path):
    #Get instagram data path and find its files.
    print("Preparing Instagram")
    dir_list = os.listdir(in_path)
    corpus_utils.make_directory(out_path)
    corpus_utils.make_directory(out_path+'all/')
    corpus = open(out_path + 'all/normalized.txt', "w", encoding="UTF8")

    #Normalize instagram data.
    for subject in dir_list:
        subject_full_path = out_path+subject+"/";
        if os.path.isdir(in_path + subject):
            corpus_utils.make_directory(subject_full_path)
            subject_file = open(subject_full_path + "normalized.txt", "w+", encoding="UTF8")
            c = 0
            for tag in os.listdir("{}{}/".format(in_path,subject)):
                if tag.endswith(".txt"):
                    #tag_full_path = "{}{}/{}".format(out_path, subject, tag);
                    #tag_file = open(tag_full_path + "_normalized.txt", "w+", encoding="UTF8")
                    print("reading {}/{}".format(subject, tag))
                    with open("{}{}/{}".format(in_path, subject, tag), encoding="UTF8") as input_file:
                        content = input_file.read()
                        posts = content.split("<instagram_post>")
                        for post in posts:
                            post = post.strip()
                            post = normalize_instagram_post(post)
                            for line in post.split('\n'):
                                line = prepare_line(line)
                                if not(re.match(r"^[^ا-ی]*$", line)) and len(line) > 1:
                                    #tag_file.write(line+"\n")
                                    subject_file.write(line+"\n")
                                    corpus.write(line+"\n")
                            #tag_file.write('<instagram_post>\n')
                            subject_file.write('<instagram_post>\n')
                            corpus.write('<instagram_post>\n')
                            c += 1
                            if c % 1000 == 0:
                                print(c, " Instagram in progress")

def normalize_instagram_post(post):
    post = re.sub(r"[^آئ\sا-ی۰-۹a-zA-Z\d؛؟…;@.!#?_:‧]", ' ', post)
    post = re.sub(r'[٪٫٬]', ' ', post)
    post = re.sub("#", " #", post)
    post = re.sub(r'[؛؟…;@\.!\?\-:‧]', '.', post)
    post = re.sub(r"(#\S+)\s", r"\n\1\n", post)
    post = re.sub(r'@\S+', '', post)

    return post

