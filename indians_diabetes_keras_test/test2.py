import numpy
import keras.models

inp = numpy.array([[float(x) for x in input('Строка: ').split(',')]])
model = keras.models.load_model('model')
pred = model.predict(inp)
print(pred[0])