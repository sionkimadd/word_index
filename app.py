from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import backend_integration as bi
import os
 
app = Flask(__name__)
 
@app.route("/")
def index():
    
    return render_template("index.html")
 
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()
    query = data.get("query")
    interval = data.get("interval")
 
    output_csv = bi.fetch_google_news(query, interval)
    bi.save_database(output_csv)
    output_sql_csv = bi.database_to_csv(query)
    output_sql_csv = bi.sort_csv_by_datetime(output_sql_csv)
    output_sentiment_csv = bi.analyze_sentiment_nltk(output_sql_csv)
    output_sentiment_csv = bi.insert_datetime(output_sql_csv, output_sentiment_csv)
    output_info_csv = bi.insert_compound(output_sentiment_csv, output_sql_csv)
    bi.plotter_sentiment_nltk(query, output_sentiment_csv)
 
    generated_files = [
        output_csv, output_sql_csv,output_sentiment_csv, output_info_csv
    ]
 
    return jsonify({
        "generated_files": generated_files,
        "sentiment_plot_path": url_for("static", filename = f"png/sentiment_plot_{query}.png")
    })
 
@app.route("/generated_files/<generated_file>", methods = ["GET"])
def download_file(generated_file):
    server_dir = os.getcwd()
    return send_from_directory(server_dir, generated_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)