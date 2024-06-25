import tensorflow as tf
from Generator import Generator
from tensorflow.keras.models import Model

generator = Generator()

train_sample, train_labels = generator.generate(1000, 3, "partial")

test_sample, test_labels = generator.generate(1000, 3, "partial")
print(train_sample.shape)




"""""
train_labels = train_labels[:, 0]
test_labels = test_labels[:, 0]
model = tf.keras.Sequential([
    tf.keras.layers.Dense(15),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_absolute_error',
              metrics=['accuracy'])

model.fit(train_sample, train_labels, epochs=10)


test_loss, test_acc = model.evaluate(test_sample,  test_labels, verbose=2)

print('\nTest accuracy:', test_acc)


x = SomeLayer(blablabla)(inp) 
x = SomeOtherLayer(blablabla)(x) #here, I just replace x, because this intermediate output is not interesting to keep


#here, I want to keep the two different outputs for defining the model
#notice that both left and right are called with the same input x, creating a fork
out1 = LeftSideLastLayer(balbalba)(x)    
out2 = RightSideLastLayer(banblabala)(x)


#here, you define which path you will follow in the graph you've drawn with layers
#notice the two outputs passed in a list, telling the model I want it to have two outputs.
model = Model(inp, [out1,out2])
model.compile(optimizer = "adam") #loss can be one for both sides or a list with different loss functions for out1 and out2    

model.fit(train_sample,train_labels, epochs=..., batch_size=...)
"""""