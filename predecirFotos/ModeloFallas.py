# El módulo permite acceder a funcionalidades del Sistema Operativo.
import os
""" Matplotlib es una biblioteca completa para crear visualizaciones 
estáticas, animadas e interactivas en Python."""
import matplotlib.pyplot as plt
# Librería de Redes Neuronales
import tensorflow as tf

# Ruta donde se encuentran los datos de entrenamiento (80% del total de los datos).
train_dataset_fp = "C:/Users/56975/Pictures/TensorFlowEntrenamiento2.txt"

#Nombre de las columnas de los datos.
column_names = ['BOMBA_FUNCIONANDO', 'PRESION_AGUA_SELLO', 'FLUJO_AGUA_SELLO', 'VELOCIDAD', 'FLUJO_TRANSMISOR', 'DENSIMETRO_NUCLEAR', 
                'V_VELOCIDAD', 'ACELERACION', 'TEMPERATURA', 'FALLAS']


feature_names = column_names[:-1] # Campos de características (No incluye la columna FALLAS).
label_name = column_names[-1] # Campo de FALLAS.

# Tipos de fallas.
class_names = ['Fuga / Filtracion Ducto descarga', 'Falla de lubricación', 'Falla de rodamientos', 
               'Detención por falla de rodamientos eje motor trabado', 'Desalineamiento', 
               'Desalineamiento+desgaste de correas', 'Corte de correas', 'Alerta de vibración/revisar causa',
               'Soltura no vnculada a rodamiento', 'Soltura falla inminente de componente', 'Falla de compopnente',
               'Correcto funcionamiento']

# Parametros de configuración de la Red Neuronal.
epocas = 201 # Número de veces a iterar el entrenamiento neuronal.
batch_size = 1 # Número de datos a procesar en cada uno de los pasos.
tasaAprendizaje = 0.0001 # Ajustes de la tasa de aprendizaje para el descenso de gradiente. 0.01


# tf.data.experimental.make_csv_dataset Analiza los datos del formato csv.
""" - Dado que el conjunto de datos esta en un archivo de texto, 
      se usa la función 'tf.data.experimental.make_csv_dataset'
      para la utilización de los datos.

    - El resultado son matrices (tensores) que almacenan cantidades de datos definidos 
      por el batch_size. En otras palabras, se dividen los datos de entrenamiento 
      en conjuntos de datos.
    """
train_dataset = tf.data.experimental.make_csv_dataset(
    train_dataset_fp, # Ruta de la ubicación del archivo txt 
    batch_size,
    column_names=column_names, # ['BOMBA_FUNCIONANDO', 'PRESION_AGUA_SELLO'... , 'TEMPERATURA']
    label_name=label_name, # [FALLAS]
    num_epochs=1)

# Itera las matrices separando los features y labels.
features, labels = next(iter(train_dataset))

""" Función que empaqueta el diccionario de características en una única matriz.
    - Toma los valores de una lista de tensores y crea un tensor combinado.
    - Se sigue respetando la cantidad de datos por lotes (batch_size). """
def pack_features_vector(features, labels):
  """ El método 'tf.stack' toma los valores de una lista de tensores 
    y crea un tensor combinado en la dimensión especificada."""
  features = tf.stack(list(features.values()), axis=1)
  return features, labels

# Empaqueta la matriz en un conjunto de datos de entrenamiento.
train_dataset = train_dataset.map(pack_features_vector)

# Itera los datos del conjunto de entrenamiento separando los features y labels.
features, labels = next(iter(train_dataset))
#print(features[:5])  # Visualizar features (Opcional).


""" MODELO DE LA RED NEURONAL.
    Dense implementa la operación:
    - output = activation(dot(input, kernel) + bias)
      - Se utiliza la función de activación ReLu. 
      - El kernel es una matriz de pesos (weights) creada por la capa. """
model = tf.keras.Sequential([
  tf.keras.layers.Dense(768, activation=tf.nn.relu, input_shape=(9,)),  # input shape required
  #tf.keras.layers.Dense(108, activation=tf.nn.relu),
  #tf.keras.layers.Dense(96, activation=tf.nn.relu),
  tf.keras.layers.Dense(384, activation=tf.nn.relu),
  tf.keras.layers.Dense(192, activation=tf.nn.relu),
  tf.keras.layers.Dense(96, activation=tf.nn.relu),
  tf.keras.layers.Dense(48, activation=tf.nn.relu),
  tf.keras.layers.Dense(24, activation=tf.nn.relu),
  tf.keras.layers.Dense(12)
])

#print(model.weights) # Visualizar los pesos del modelo asignados aleatoria mente (Opcional).


""" ENTRENAR LA RED NEURONAL """

""" El modelo calculará su pérdida usando la función Categorical Cross-Entropy:
    - Es utilizada cuando existen múltiples clases y asigna un valor de probabilidad determinada por 
      la suma del polinomio logarítmico que otorga a cada clase cuanta probabilidad de predicción 
      tuvo la red neuronal."""

loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

""" Función de perdida.
    Tanto la etapa de entrenamiento como la de evaluación deben calcular la pérdida del modelo. 
    La función de perdida verifica la diferencia entre el valor predicho y el valor real, en otras 
    palabras, qué tan mal está funcionando el modelo. Queremos minimizar u optimizar este valor. """

def loss(model, x, y, training):
  # training=training is needed only if there are layers with different
  # behavior during training versus inference (e.g. Dropout).
  y_ = model(x, training=training)
  return loss_object(y_true=y, y_pred=y_)

""" Función de gradiente """

def grad(model, inputs, targets):
  with tf.GradientTape() as tape:
    loss_value = loss(model, inputs, targets, training=True)
  return loss_value, tape.gradient(loss_value, model.trainable_variables)

""" DESCENSO DEL GRADIENTE 
    - Se utilizará el descenso de gradiente estocástico 'Stochastic Gradient Descendent (SGD)'.
    - Se define la tasa de crecimiento (learning_rate). """
optimizer = tf.keras.optimizers.SGD(learning_rate=tasaAprendizaje)  #taza de aprendizaje


""" BUCLE DE ENTRENAMIENTO """
train_loss_results = []
train_accuracy_results = []

num_epochs = epocas

for epoch in range(num_epochs):
  epoch_loss_avg = tf.keras.metrics.Mean()
  epoch_accuracy = tf.keras.metrics.SparseCategoricalAccuracy()
  # Bucle de entrenamiento usando lotes definidos por el batch_size.
  for x, y in train_dataset:
    # Optimiza el modelo con el descenso de gradiente estocástico (SGD).
    loss_value, grads = grad(model, x, y)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))

    # Sigue el proceso.
    epoch_loss_avg(loss_value)  # Add current batch loss
    """ Compara la etiqueta predicha con la etiqueta real.
        training = true, si son diferente las etiquetas. """
    epoch_accuracy(y, model(x, training=True))

  # Última epoca.
  train_loss_results.append(epoch_loss_avg.result())
  train_accuracy_results.append(epoch_accuracy.result())

  if epoch % 50 == 0:
    print("Epoch {:03d}: Loss: {:.3f}, Accuracy: {:.3%}".format(epoch,
                                                                epoch_loss_avg.result(),
                                                                epoch_accuracy.result()))

""" Visualización opcional de la función de perdida a lo largo del entrenamiento (Opcional). """
fig, axes = plt.subplots(2, sharex=True, figsize=(12, 8))
fig.suptitle('Training Metrics')

axes[0].set_ylabel("Loss", fontsize=14)
axes[0].plot(train_loss_results)

axes[1].set_ylabel("Accuracy", fontsize=14)
axes[1].set_xlabel("Epoch", fontsize=14)
axes[1].plot(train_accuracy_results)
plt.show()


""" EVALUAR LA EFECTIVIDAD DEL MODELO CON LOS DATOS DE VALIDACIÓN.
    - Recordar que los datos se dividen en un 80% datos de entrenamiento y
      20% datos de validación. """

""" CONFIGURAR EL CONJUNTO DE DATOS DE PRUEBA. 
    Evaluar el modelo es similar a entrenarlo. Para evaluar de manera justa la efectividad 
    de un modelo, los ejemplos usados ​​para evaluar un modelo deben ser diferentes de los 
    ejemplos usados ​​para entrenar el modelo. """

# Ruta donde se encuentran los datos de validación (20% del total de los datos).
test_fp = "C:/Users/56975/Pictures/TensorFlowValidacion.txt"

test_dataset = tf.data.experimental.make_csv_dataset(
    test_fp,
    batch_size,
    column_names=column_names,
    label_name='FALLAS',
    num_epochs=1,
    shuffle=False)

test_dataset = test_dataset.map(pack_features_vector)

test_accuracy = tf.keras.metrics.Accuracy()

#aquí
for (x, y) in test_dataset:
  # training=False is needed only if there are layers with different
  # behavior during training versus inference (e.g. Dropout).
  logits = model(x, training=False)
  prediction = tf.argmax(logits, axis=1, output_type=tf.int32)
  test_accuracy(prediction, y)
  print(tf.stack([y,prediction],axis=1)) # Visualizar los valores reales y los predichos.

print("Exactitud del conjunto de validación: {:.3%}".format(test_accuracy.result()))


""" ***** GUARDAR EL ENTRENAMIENTO DE LA RED NEURONAL ***** """
#target_dir = 'C:/Users/56975/Desktop/ProyectoDjango/redesneuronales/modelos'
#if not os.path.exists(target_dir):
#  os.mkdir(target_dir)
#model.save('C:/Users/56975/Desktop/ProyectoDjango/redesneuronales/modelos/modeloFallas.h5')
#model.save_weights('C:/Users/56975/Desktop/ProyectoDjango/redesneuronales/modelos/pesosFallas.h5')


""" ***** USA EL MODELO ENTRENADO PARA HACER PREDICCIONES. ***** """
#Soltura falla inminente de componente
predict_dataset = tf.convert_to_tensor([
    [1, 685.84, 5.19, 65.73, 202.03, 1.71, 12.945, 40.155, 35.315]
])

# training=False is needed only if there are layers with different
# behavior during training versus inference (e.g. Dropout).
predictions = model(predict_dataset, training=False)

for i, logits in enumerate(predictions):
  class_idx = tf.argmax(logits).numpy()
  p = tf.nn.softmax(logits)[class_idx]
  name = class_names[class_idx]
  
  print("Example {} prediction: {} ({:4.1f}%)".format(i, name, 100*p))

""" Aquí, cada ejemplo devuelve un logit para cada clase.
    Para convertir estos logits en una probabilidad se utiliza 
    la función softmax """
