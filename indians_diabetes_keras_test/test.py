from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
import numpy

# задаем для воспроизводимости результатов
numpy.random.seed(2)

# загружаем датасет, соответствующий последним пяти годам до определение диагноза 
dataset = numpy.loadtxt("prima-indians-diabetes.csv", delimiter=",")
testset = numpy.loadtxt("test.csv",delimiter=",")
# разбиваем датасет на матрицу параметров (X) и вектор целевой переменной (Y)
X, Y = dataset[:, 0:8], dataset[:, 8]
X_t, Y_t = testset[:, 0:8], testset[:,8]

# создаем модели, добавляем слои один за другим
model = Sequential()
model.add(Dense(10, input_dim=8, activation='relu'))  # входной слой требует задать input_dim
model.add(Dense(100, activation='relu'))
#model.add(Dense(100, activation='sigmoid'))
#model.add(Dense(10, activation='relu'))
model.add(Dense(1, activation='sigmoid'))  # сигмоида вместо relu для определения вероятности

# компилируем модель, используем градиентный спуск adam
model.compile(loss="binary_crossentropy", optimizer=optimizers.adam(), metrics=['accuracy'])

# обучаем нейронную сеть
model.fit(X, Y, epochs=100, batch_size=100)

# оцениваем результат
scores = model.evaluate(X_t, Y_t)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
model.save('model')

