import re
import sys
import os
import argparse

"""
Creates a dictionary of abreviations
"""
def make_abrev_dict():
    abreviations = open("skammstafanir.txt", "r")
    abrev_dict = dict()
    for abrev in abreviations:
        abrev_dict.update({f'{abrev}':f'{abrev}'})
    return abrev_dict

def better_clean(tokens, abrev_dict):
    tokens = re.sub(",$", "\n,", tokens)
    tokens = re.sub(":$", "\n:", tokens)
    #ATH hvort token er lén, stytting eða email
    if(re.match(".+(://)...+", tokens) or (tokens in abrev_dict) or re.match(".+\@.+\..+", tokens) or re.match("[0-9]+[\.,][0-9]*", tokens)): #Gerum ráð fyrir að lén sé aldrei styttra en 
        return tokens
    else:
        tokens = re.sub("-$", "\n-", tokens)
        tokens = re.sub("\.$", "\n.", tokens)
        if(re.search("[0-9][\-\+\*=/][0-9]", tokens)): #Gerum ráð fyrir að 1-3 og aðrar slíkar segðir séu ekki leyfilegir tokenar
            tokens = re.sub("-", "\n-\n", tokens)
            tokens = re.sub("\+", "\n+\n", tokens)
            tokens = re.sub("\*", "\n*\n", tokens)
            tokens = re.sub("=", "\n=\n", tokens)
            tokens = re.sub("/", "\n/\n", tokens)
        return tokens

def initial_cleaning(line):
    symbols = "[()]}{?!]" #tákn sem ættu aldrei að vera hluti af tokeni
    reconstucted = ""
    for word in line.split():
        for symbol in symbols:
            if(symbol in word):
                torn = word.split(symbol)
                word = torn[0] +" "+ symbol + " " + torn[1]
        reconstucted = reconstucted + " " + word
    return reconstucted 

def master_clean_text(text, output_name):
     out = open(output_name, "w+", encoding="utf-8")
     token = ""
     abreviation_dict = make_abrev_dict()
     for items in text:
        for item in initial_cleaning(items).split(" "):
            item = re.sub(r"\s", "", item)
            match = re.search("[\.,_:“„;'\+\*\-\[\]\{\}()//~\?!&%#^<>|’=`ˈ]", item) #Vitum núna að við þurfum að skoða nánar
            if not match:
                token = item
            else:
                token = better_clean(item, abreviation_dict)
            if token is not "" or re.match("\s",token):
                out.write(f'{token}\n')
        out.write(f'\n') #Auka línubil eftir hverja málsgrein

def run(args):
    text_file = open(args.input, encoding="utf-8")
    out_file_name = "tokenized.txt"
    if args.output is not None:
        out_file_name = args.output
    master_clean_text(text_file.readlines(), out_file_name)

def main():
    parser=argparse.ArgumentParser(description="Tokenizer")
    parser.add_argument("-in",help="text file name" ,dest="input", type=str, required=True)
    parser.add_argument("-out",help="tokenized output filename", dest="output", type=str, required=False)
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)

if __name__=="__main__":
    main()