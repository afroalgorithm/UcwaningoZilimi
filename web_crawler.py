from tkinter import *
from bs4 import BeautifulSoup
import urllib.request
import requests
import random

def get_article_links():    
    parser = 'html.parser'  
    links = []

    #GET BAYEDE NEWS LINKS
    resp = urllib.request.urlopen("https://bayedenews.com/")
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('https://bayedenews.com/20'):
            links.append(link['href'])

    #GET ILANGA NEWS LINKS
    resp = urllib.request.urlopen("https://ilanganews.co.za/")
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('https://ilanganews.co.za/') and not 'category' in link['href'] and not 'author' in link['href']:
            links.append(link['href'])

    return links

def get_article_content():
    
    article_content = []
    article_links = random.sample(get_article_links(), 50) #ADJUST THIS NUMBER 50 TO INCR/DECR THE NUMBER OF ARTICLES SEARCHED
    for link in article_links:
        html_content = requests.get(link).text
        soup = BeautifulSoup(html_content, "lxml")
        article_text = ''
        if link.startswith('https://bayedenews.com/'):
            
            article = soup.find("div", {"class":"post-content entry-content"}).findAll('p')
            for element in article:
                article_text += '\n' + ''.join(element.findAll(text = True))
                
            article_content.append(article_text)
        else:
            try:
                article = soup.find("div", {"class":"td-post-content tagdiv-type"}).findAll('p')
                for element in article:
                    article_text += '\n' + ''.join(element.findAll(text = True))
                    
                article_content.append(article_text)
            except Exception:
                print(link)
            

    return article_content

def generate_corpus():
   definition_label.configure(text='Generating corpus. . . Please wait. This could take up to 4 minutes')
   
   global result
   result = str(entry.get()).strip().lower()
   res = [ele for ele in get_article_content() if(result in ele)]
   
   if res:
       f = open('corpus.txt', 'w')
       for article in res:
           f.write(article)
           f.write('\n\n')
       f.close()
       message = "Your corpus has been generated"
   else:
       message = "We couldn't find the word you entered"
         
   definition_label.configure(text=message)


root = Tk()
root.geometry("800x400")
root.configure(bg='orange')
root.title('Mthuli Bethelezi')

label = Label(root, bg='orange', fg='#fff',
              text='IsiZulu Web Crawler',
              font=("Helvetica", 12), pady=30)
label.pack()
entry = Entry(root, bd=5, width=50)
entry.pack()
space_label1 = Label(root, bg='orange', fg='#fff',)
space_label1.pack()
button = Button(root, text="Generate Corpus", command=generate_corpus, width=20)
button.pack()
space_label = Label(root, bg='orange', fg='#fff')
space_label.pack()
definition_label = Label(root, bg='orange', fg='#fff',
            font=("Helvetica", 12))
definition_label.pack()
root.mainloop()
