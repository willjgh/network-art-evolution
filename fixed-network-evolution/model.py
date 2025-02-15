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
    
    def radial(self, x):
        '''Radial activation function'''
        return self.softplus(x - np.mean(x))

    def initialize_parameters(self):
        '''Initialize model parameters with uniformly distributed values.'''

        # activation options
        self.activations_available = [self.radial, self.softplus, self.sigmoid, self.relu, np.sin, np.cos]

        # for each layer
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
                activation = rng.choice(self.activations_available)
                self.activations.append(activation)

    def forward(self, x):
        '''Forward pass over model with input x.'''

        # pass x through network layers
        for i in range(self.depth - 1):
            x = self.weights[i] @ x + self.biases[i][:, None]
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
    
    def colour_batch(self, height, width):
        '''Get colour given array of pixels.'''

        # array of coordinates in batch as 2 x (height * width) array
        x = np.array([(i, j) for i in range(height) for j in range(width)]).T
        
        # pass through model
        model_output = self.forward(x)

        # reshape to grid
        model_output = model_output.reshape(3, height, width)

        # move RGB dimension to last
        colours = np.transpose(model_output, (1, 2, 0))

        # convert to int [0, 255]
        colours = (colours * 255).astype(np.int32)

        return colours