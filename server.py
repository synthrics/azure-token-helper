from flask import Flask, jsonify
import subprocess, json, time

app = Flask(__name__)

cache = {"token": None, "expires_at": 0}


def _az_get_access_token():
    result = subprocess.run(
        ["az", "account", "get-access-token"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "").strip() or "az exited with code %s" % result.returncode
        return None, err
    raw = (result.stdout or "").strip()
    if not raw:
        return None, (result.stderr or "").strip() or "az produced no output"
    try:
        return json.loads(raw), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON from az: %s" % e


@app.route("/token")
def get_token():
    now = time.time()

    if cache["token"] and now < cache["expires_at"] - 60:
        return jsonify({"token": cache["token"]})

    data, err = _az_get_access_token()
    if err is not None:
        return jsonify({"error": err}), 502
    cache["token"] = data["accessToken"]
    # Azure returns expiry as a datetime string, simpler to just cache for 50 mins
    cache["expires_at"] = now + 3000

    return jsonify({"token": cache["token"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)