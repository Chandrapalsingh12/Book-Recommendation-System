from flask import Flask,render_template,request,redirect
import pickle
import numpy as np


app = Flask(__name__)
top_50_books = pickle.load(open("top_50.pkl","rb"))
book_name = pickle.load(open("book_name.pkl","rb"))

pt = pickle.load(open("pt.pkl","rb"))
book = pickle.load(open("book.pkl","rb"))


similarity_score = pickle.load(open("similarity.pkl","rb"))


''''Book-Title', 'no_of_rating', 'avg_rating', 'Book-Author',
       'Image-URL-L'''

@app.route("/")
def Home():

    return render_template("index.html",
    book_title = list(top_50_books["Book-Title"].values),
    book_author = list(top_50_books["Book-Author"].values),
    rating = list(top_50_books["no_of_rating"].values),
    img_url = list(top_50_books["Image-URL-L"].values),
    book_name = book_name  
    )

@app.route("/recom",methods=["GET","POST"])
def recommended():
    if request.method=="POST":
        book_names = request.form.get("bname")
        index = np.where(pt.index==book_names)[0][0]
        similar_items = sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]
        data = []
        for i in similar_items:
            item = []
            temp_df = book[book["Book-Title"]==pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-L"].values))
            data.append(item)
        print(data)


        # print(b_name)


        return render_template("recomended.html",book_name =book_name,data=data,book_names=book_names)
    else:
        return redirect("/")

def Recommen(book_name):
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = book[book["Book-Title"]==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-L"].values))
        data.append(item)
    return data



if __name__=="__main__":
    app.run(debug=True)

