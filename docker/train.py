import os
import matplotlib.pyplot as plt
from mediapipe_model_maker import gesture_recognizer
import shutil
import os
import tensorflow as tf

class ModelTrainer():
    @staticmethod
    def train():

        dataset_path = 'Samples'
        shutil.copytree('NONE', 'Samples/NONE')

        print(dataset_path)
        labels = []
        for i in os.listdir(dataset_path):
            if os.path.isdir(os.path.join(dataset_path, i)):
                labels.append(i)
        print(labels)



        data = gesture_recognizer.Dataset.from_folder(
            dirname=dataset_path,
            hparams=gesture_recognizer.HandDataPreprocessingParams(),
        )
        train_data, rest_data = data.split(0.7)
        validation_data, test_data = rest_data.split(0.8)


        model_options = gesture_recognizer.ModelOptions(
            dropout_rate = 0.2,
            layer_widths = [256, 256, 128, 64]
        )

        hparams = gesture_recognizer.HParams(batch_size=8, 
                                             epochs=8, 
                                             shuffle= True ,
                                             export_dir='exported_model'
                                             )
        options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams, model_options=model_options)

        model = gesture_recognizer.GestureRecognizer.create(
            train_data=train_data,
            validation_data=validation_data,
            options=options
        )


        loss, acc = model.evaluate(test_data, batch_size=2)
        print(f'Test loss: {loss}, Test accuracy: {acc}')

        if(os.path.exists('gesture_recognizer.task')):
            os.remove('gesture_recognizer.task')

        model.export_model()

        shutil.move('exported_model/gesture_recognizer.task', './')
        shutil.rmtree('exported_model')
        shutil.rmtree('Samples')