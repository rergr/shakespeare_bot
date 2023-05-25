# shakespeare_bot
Shakespeare bot is an ai that's capable of writing texts in the style of shakespeare, essentially continiuing his legacy.


![grafik](https://github.com/rergr/shakespeare_bot/assets/132651459/d13c4ebe-ce6f-4d8f-ba91-607e187de39c)
Classification Neural Network
Description

This project is a versatile neural network package specifically designed for classification tasks. It can be used for training various deep learning models, including image recognition. The package includes an example project for MNIST classification to demonstrate its capabilities. With its flexible architecture, the package is suitable for a range of classification tasks requiring deep learning, offering high accuracy and reliability.
Getting Started
Dependencies

    numpy
    matplotlib
    albumentations
    scikit-learn
    jupyter
    scipy
    scikit-image
    pillow
    customtkinter

Installing

    Clone the repository
    Navigate to the package directory
    Run pip install . to install package

or

    Run pip install git+https://github.com/Havilash/Neural-Network.git#egg=neural_network to install package

Executing program

    Import package

from neural_network import activations, costs, nn as neural_network, layers, gui, constants
from neural_network.data import get_mnist_data, get_augmented_mnist_data, train_test_split
from neural_network.filters import ALL_FILTERS

    Run example project python ./neural_network/main.py or python -m neural_network.main

Authors

    @Havilash
    @Gregory
    @Nicolas
    @Ensar

License

see the LICENSE file for details
