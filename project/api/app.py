from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

# Lisans anahtarları
licenses = {
    "USER123": {"expires": datetime(2025, 2, 1), "active": True},
    "TEST456": {"expires": datetime(2025, 1, 15), "active": True},
}

@app.route("/validate", methods=["POST"])
def validate_license():
    data = request.json
    license_key = data.get("license_key")

    if license_key not in licenses:
        return jsonify({"valid": False, "message": "Lisans anahtarı geçersiz!"})

    license_info = licenses[license_key]
    if not license_info["active"]:
        return jsonify({"valid": False, "message": "Lisans anahtarı pasif durumda!"})

    if datetime.now() > license_info["expires"]:
        return jsonify({"valid": False, "message": "Lisans süresi dolmuş!"})

    return jsonify({"valid": True, "message": "Lisans geçerli!"})

@app.route("/add_license", methods=["POST"])
def add_license():
    data = request.json
    license_key = data.get("license_key")
    duration_days = data.get("duration_days", 30)

    if not license_key:
        return jsonify({"success": False, "message": "Lisans anahtarı gerekli!"})

    if license_key in licenses:
        return jsonify({"success": False, "message": "Bu lisans zaten mevcut!"})

    licenses[license_key] = {
        "expires": datetime.now() + timedelta(days=duration_days),
        "active": True
    }
    return jsonify({"success": True, "message": "Lisans başarıyla eklendi!"})

@app.route("/delete_license", methods=["POST"])
def delete_license():
    data = request.json
    license_key = data.get("license_key")

    if not license_key or license_key not in licenses:
        return jsonify({"success": False, "message": "Lisans bulunamadı!"})

    del licenses[license_key]
    return jsonify({"success": True, "message": "Lisans başarıyla silindi!"})

@app.route("/list_licenses", methods=["GET"])
def list_licenses():
    result = {
        key: {
            "expires": info["expires"].strftime("%Y-%m-%d"),
            "active": info["active"]
        }
        for key, info in licenses.items()
    }
    return jsonify(result)

@app.route("/")
def index():
    return jsonify({"message": "Flask uygulaması çalışıyor!"})

if __name__ == "__main__":
    app.run(debug=True)
