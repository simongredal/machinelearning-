import base64
import io
import pdb
from flask import Flask, render_template, request
from keras.models import load_model
from keras.utils import load_img, img_to_array
import numpy as np
from PIL import Image

app = Flask(__name__)

model = load_model('mymodel.h5')


# will use get for the first page-load, post for the form-submit
@app.route('/', methods=['post', 'get'])
# this function can have any name
def predict():
    try:
        # pdb.set_trace()

        image_dataurl = request.form.get('image')

        if image_dataurl is None:
            # calling render_template will inject the variable 'result' and send index.html to the browser
            return render_template('index.html', most_likely='none', second_likely='none', result='No input(s)')
        else:
            raw_image = Image.open(io.BytesIO(base64.b64decode(image_dataurl.replace("data:image/png;base64,", ""))))\
                .convert('L').resize((28, 28))

            array_image = img_to_array(raw_image)
            rescaled_image = np.multiply(1. / 255, array_image)
            expanded_image = np.expand_dims(rescaled_image, axis=0)
            images = np.vstack([expanded_image])

            # make new prediction
            predictions = model.predict(images)

            # the result is set, by asking for row=0, column=0. Then cast to string.
            sorted_args = np.argsort(predictions[0])
            most_likely = sorted_args[9]
            second_likely = sorted_args[8]

            result = np.round(predictions[0], decimals=2)

            return render_template('index.html', most_likely=most_likely, second_likely=second_likely, result=str(result))
    except Exception as e:
        return render_template('index.html', most_likely='error', second_likely='error', result='error ' + str(e))


if __name__ == '__main__':
    app.run()
