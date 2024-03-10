from flask import Flask , send_from_directory
from flask_flatpages import FlatPages
from flask import render_template
import os
import random


FLATPAGES_EXTENSION = '.md'
FLATPAGES_AUTO_RELOAD = True

app = Flask(__name__) 
app.config['APPLICATION_ROOT'] = '/776'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FLATPAGES_MARKDOWN_EXTENSIONS = ['extra']
FLATPAGES_EXTENSION_CONFIGS = {
   'codehilite': {
       'linenums': 'True'
   }
}

app.config.from_object(__name__)
pages = FlatPages(app)
application = app
pages.get('foo')


def Liste_cat():
  articles = (p for p in pages if 'published' in p.meta)
  catList = set()
  for a in articles:
      if 'cat' in a.meta:
          catList.add(a.meta['cat'])
  catList = list(dict.fromkeys(catList))
  return catList

def Liste_authors():
 articles = (p for p in pages if 'published' in p.meta)
 authorsList = set()
 for a in articles:
     if 'author' in a.meta:
         authorsList.add(a.meta['author'])
 authorsList = list(dict.fromkeys(authorsList))
 return authorsList


def imagelist(articlename):
 dir_path = os.path.join(BASE_DIR, 'pages', articlename)
 if os.path.exists(dir_path):
     images = [f for f in os.listdir(dir_path) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('.gif') or f.endswith('.svg')]
     # Create relative paths
     images = ["pages/" + articlename + "/" + img for img in images]
     return articlename, images
 else:
     return None, None

def get_random_image():
    images_dir = os.path.join(BASE_DIR, 'static', 'img', 'home-image')
    images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg'))]
    if images:
        return 'img/home-image/' + random.choice(images) # Ajoutez 'img/' au début du chemin
    else:
        return 'img/default.png' # Assurez-vous que 'default.png' existe dans 'static/img'

def get_random_article():
    # Sélectionner un article aléatoire parmi tous les articles publiés
    articles = [p for p in pages if 'published' in p.meta]
    if articles:
        # Sélectionner un article aléatoire
        random_article = random.choice(articles)
        # Préparer les informations de l'article pour l'affichage
        article_info = {
            'title': random_article.title,
            'author': random_article.meta.get('author', ''),
            'published': random_article.meta.get('published', '').strftime('%Y') if random_article.meta.get('published', '') else '',
            'desc': random_article.meta.get('desc', ''),
            'cover': random_article.meta.get('cover', 'img/def.jpg')
        }
        return article_info
    # Si aucun article n'a été trouvé, retourner une valeur par défaut
    return {
        'title': 'No articles found',
        'author': '',
        'published': '',
        'desc': '',
        'cover': 'img/default.png'
    }


@app.route('/<path:path>')
def page(path):
 page = pages.get_or_404(path)
 catList = Liste_cat()
 authorsList = Liste_authors()
 g_path, imgs = imagelist(path)
 selectedAuthor = page.meta.get('author', '') # Ajoutez cette ligne
 articles = (p for p in pages if 'published' in p.meta) # Ajoutez cette ligne
 if imgs:
     return render_template('single.html', page=page ,catList=catList, authorsList=authorsList, g_path=g_path, imgs = imgs, selectedAuthor=selectedAuthor, articles=articles) # Modifiez cette ligne
 else :
     return render_template('single.html', page=page ,catList=catList,authorsList=authorsList, selectedAuthor=selectedAuthor, articles=articles) # Modifiez cette ligne


@app.route('/info')
def info():
   page = pages.get_or_404('info')
   catList = Liste_cat()
   return render_template('staticpage.html', page=page , catList=catList)

@app.route('/cat/<catname>') 
def catPage(catname):
 articles = (p for p in pages if 'published' in p.meta and 'cat' in p.meta and p.meta['cat']==catname )
 latest = sorted(articles, reverse=True,
               key=lambda p: p.meta['published'])
 catList = Liste_cat()
 authorsList = Liste_authors() # Et celle-ci
 
 return render_template('index.html', articles=latest , catList=catList, authorsList=authorsList )

@app.route('/author/<path:authorname>')
def authorPage(authorname):
 author_names = authorname.split('+')
 articles = [p for p in pages if 'published' in p.meta and 'author' in p.meta and p.meta['author'] in author_names]
 latest = sorted(articles, reverse=True,
               key=lambda p: p.meta['published'])
 catList = Liste_cat()
 authorsList = Liste_authors()
 selectedAuthor = authorname # Définir la variable ici
 return render_template('author.html', articles=latest , catList=catList, authorsList=authorsList, selectedAuthor=selectedAuthor)



@app.route('/pages/<path:path>')
def serve_pages(path):
   return send_from_directory('pages', path)


@app.route('/')
def index():
    random_image = get_random_image()
    articles = (p for p in pages if 'published' in p.meta)
    latest = sorted(articles, reverse=True, key=lambda p: p.meta['published'])
    catList = Liste_cat()
    authorsList = Liste_authors()
    return render_template('index.html', articles=latest, catList=catList, authorsList=authorsList, random_image=random_image,)



@app.errorhandler(404)
def page_not_found(e):
       # note that we set the 404 status explicitly
           return "Problem"

if __name__ == "__main__":
       app.run(host='0.0.0.0')
