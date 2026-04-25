from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
CLEAN_FOLDER = "clean"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CLEAN_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_data(df):
    original_rows = len(df)
    original_cols = list(df.columns)

    # Remove duplicatas
    df = df.drop_duplicates()
    removed_duplicates = original_rows - len(df)

    # Remove espaços extras
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    # Conta nulos antes de preencher
    null_count = int(df.isnull().sum().sum())

    # Preenche valores nulos
    df = df.fillna("N/A")

    # Padroniza nomes das colunas
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]

    stats = {
        "original_rows": original_rows,
        "clean_rows": len(df),
        "removed_duplicates": removed_duplicates,
        "null_filled": null_count,
        "columns": len(df.columns),
    }

    return df, stats

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Nome de arquivo inválido"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Formato não suportado. Use CSV, XLSX ou XLS."}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)

        df_clean, stats = clean_data(df)

        clean_filename = "cleaned_" + os.path.splitext(file.filename)[0] + ".csv"
        clean_path = os.path.join(CLEAN_FOLDER, clean_filename)
        df_clean.to_csv(clean_path, index=False)

        return jsonify({
            "success": True,
            "stats": stats,
            "download_file": clean_filename,
            "preview": df_clean.head(5).to_dict(orient="records"),
            "columns": list(df_clean.columns),
        })

    except Exception as e:
        return jsonify({"error": f"Erro ao processar arquivo: {str(e)}"}), 500

@app.route("/download/<filename>")
def download(filename):
    clean_path = os.path.join(CLEAN_FOLDER, filename)
    if not os.path.exists(clean_path):
        return jsonify({"error": "Arquivo não encontrado"}), 404
    return send_file(clean_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
