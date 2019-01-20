from flask import Flask, request
from process_data import *
from prep_video import *
from get_data import *
from modelling import *
import json

app = Flask(__name__)

@app.route('/normalize', methods=['POST'])
def normalize():
    print('Prepping ->')
    data =  request.get_json()
    url = data['url']

    #get data
    brightness_vals, vid_frames = stream_data1(url)
    model_input = np.array(brightness_vals).reshape(-1,1)

    input_scaled = scale_data(model_input)
    input_win = make_windows(input_scaled, 24)
    input_ready = prep_for_model(input_win, 24, 1)

    #build model
    model = build_model('C:/Users/Adrian/Desktop/Hackathons/Swamp/ae_weights_24_dos.h5')

    #get predictions
    prediction = get_prediction(input_ready, model)
    anomalies = find_anomalies(input_ready, prediction, url)

    #edit the video
    new_vid = enhance_video(input_ready, prediction, anomalies, np.array(vid_frames), 30)

    #make the new video
    make_video(new_vid)

    print(anomalies)
    print(input_scaled)
    return json.dumps({"destination":'C:/Users/Adrian/Desktop/Hackathons/Swamp/safe.mp4'})

if __name__ == '__main__':
    app.run(debug=True, port = 3001)
