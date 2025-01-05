# Imports
import numpy as np

# setup
rng = np.random.default_rng()

class Model():

    def __init__(self, widths=[3, 3, 3], input_width=2, output_width=3):
        '''Initialize'''
        self.weights = []
        self.biases = []
        self.activations = []
        self.layer_widths = [input_width] + widths + [output_width]
        self.depth = len(self.layer_widths)

    def softmax(self, x):
        '''Softmax activation function.'''
        max_val = np.max(x)
        exp_x = np.exp(x - max_val)
        return exp_x / np.sum(exp_x)
    
    def sigmoid(self, x):
        '''Sigmoid activation function'''
        return 1 / (1 + np.exp(-x))
    
    def softplus(self, x):
        '''Softplus activation function.'''
        return np.log(1 + np.exp(x))

    def relu(self, x):
        '''ReLu activation function'''
        return np.maximum(x, 0)

    def initialize_parameters(self):
        '''Initialize model parameters with uniformly distributed values.'''
        for i in range(1, self.depth):

            # parameter sizes
            weight_size = (self.layer_widths[i], self.layer_widths[i - 1])
            bias_size = self.layer_widths[i]

            # uniformly distributed values
            self.weights.append(rng.uniform(-1, 1, size=weight_size))
            self.biases.append(rng.uniform(-1, 1, size=bias_size))

            # activation function
            if i == self.depth - 1:
                # final layer: sigmoid
                self.activations.append(self.sigmoid)
            else:
                # otherwise: random
                activation = rng.choice([self.softplus, self.relu, np.sin, np.cos])
                self.activations.append(activation)

    def forward(self, x):
        '''Forward pass over model with input x.'''

        # pass x through network layers
        for i in range(self.depth - 1):
            x = self.weights[i] @ x + self.biases[i]
            x = self.activations[i](x)

        return x
    
    def colour(self, i, j):
        '''Get colour given pixel location.'''

        # pass through model
        x = np.array([i, j])
        model_output = self.forward(x)

        # convert to integer [0, 255]
        red = int(model_output[0] * 255)
        green = int(model_output[1] * 255)
        blue = int(model_output[2] * 255)

        # return tuple
        return (red, green, blue)