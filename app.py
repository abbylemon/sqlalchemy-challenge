from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    print("Welcome to my home page....")
    print("For more content go to:")
    print("/api/v1.0/precipitation")
    print("/api/v1.0/stations")
    print("/api/v1.0/tobs")
    print("/api/v1.0/<start>")
    print("/api/v1.0/<start>/<end>")
    
    
    
if __name__ == '__main__':
    app.run(debug=True)