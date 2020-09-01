import time
import subprocess
from flask import Flask, request, abort, jsonify
from hydro_tools.utils import validate_json
from hydro_tools.schema import OCUSF_POST_SCHEMA

app = Flask(__name__)
OCUSF_FILE_PATH = "/ocusf"
SIMS_PATH = OCUSF_FILE_PATH + "/sims"
EXE_PATH = OCUSF_FILE_PATH + "/ocusf.exe"


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.route('/ocusf', methods=['POST'])
def ocusf_create():
    # eg curl -X POST -H "Content-Type: application/json" -d '{"config":{"shape":1,"width":3.0,"length":500.0,"manning":0.015,"slope":0.0005,"qinit":4.0,"upstream":{"type":2,"rate":0.0, "final":0.0},"downstream":{"type":1,"rate":-0.0666, "final":0.0},"reaches":10, "iterations":100}}' http://127.0.0.1/rest/ocusf
    data = request.get_json()
    err = validate_json(data, OCUSF_POST_SCHEMA)
    if err:
        abort(400, description=err)
    
    time_str = time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime())
    input_file = SIMS_PATH + "/" + time_str + ".dat"
    output_file = SIMS_PATH + "/" + time_str + ".json"
    _write_input_file(data["config"], input_file)
    _run_sim(input_file, output_file)
    results = _read_output_file(output_file)
    return results


@app.route('/ocusf', methods=['GET'])
def ocusf_get():
    message = "******Welcome to OCUSF*******" \
              "To create a simulation make a POST request to URI: ocusf.\n" \
              "To get details of the POST parameters make a GET request to ocusf/help.\n"
    return message


@app.route('/ocusf/help', methods=['GET'])
def ocusf_get_help():
    return jsonify(OCUSF_POST_SCHEMA)



def _write_input_file(inp, filename):
    f = open(filename, "w")
    f.write("OCUSF Input File\n")
    upstream = _get_boundary_conditions(inp["upstream"])
    downstream = _get_boundary_conditions(inp["downstream"])
    args = (inp["shape"], inp["width"], inp["length"], inp["manning"],
            inp["slope"], inp["qinit"], upstream, downstream, inp["reaches"], inp["iterations"])
    f.write("%d %f %f %f %f %f %s %s %d %d\n" % args)
    f.close()


def _run_sim(input_file, output_file):
    # This returns data as table via stdout but throw it away
    # because better to read json output file
    subprocess.check_output([EXE_PATH, input_file, output_file])


def _read_output_file(filename):
    f = open(filename, "r")
    all_file = f.read()
    f.close()
    return all_file


def _get_boundary_conditions(bc):
    params = str(bc["type"]) +  " " + str(bc["rate"])
    if bc["type"] == 1: # IE Flow
        params += " " + str(bc["final"])
    return params
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
