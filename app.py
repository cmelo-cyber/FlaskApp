from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)


def get_blog_posts():
    with open("blog_posts.json", "r") as file:
        blog_posts = json.load(file)
    return blog_posts




@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    blog_posts = get_blog_posts()


    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    blog_posts = get_blog_posts()

    ids = []                     #this lines are used to create the new id
    for blog in blog_posts:
        ids.append(blog["id"])
    if len(ids) == 0:
        new_id = 1
    else:
        new_id = int(max(ids)) + 1

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        blog_posts.append({
            'id': new_id,
            'title':title,
            'author':author,
            'year':year})

        with open("blog_posts.json", "w", encoding="utf-8") as file:
            json.dump(blog_posts, file)

        return redirect('/')

    return render_template('add.html')

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id): # wir nehmen die id auf für die die änderung gemacht werden soll
    blog_posts = get_blog_posts()

    for blog in blog_posts: # weil blog_post eine liste ist müssen wir durch iterieren um den richtigen blog zu finden
        if post_id == blog['id']:

            if request.method == 'POST':
                blog["title"] = request.form['title']
                blog["author"] = request.form['author']
                blog["year"] = request.form['year']

                with open("blog_posts.json", "w", encoding="utf-8") as file:
                    json.dump(blog_posts, file)

                return redirect('/')
        # Falls es nur ein get method war dann wird
        # die Seite aufgerufenum die alten Daten im Eingabefeld anzeigen
        # zu können müssen wir blog an das Template übergeben
        return render_template('update.html', blog=blog)
    return "Blog nicht gefunden", 404

@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = get_blog_posts()

    for blog in blog_posts:
        if post_id == blog['id']:
            blog_posts.remove(blog)
            break

    with open("blog_posts.json", "w", encoding="utf-8") as file:
        json.dump(blog_posts, file)
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)