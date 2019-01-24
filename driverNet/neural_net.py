import random
from utils import sigmoid
import config as c

class NeuralNet():
    def __init__(self, hidden_neurons):
        self.inputs = 5
        self.hidden_neurons = hidden_neurons
        self.outputs = 2

        self.init_weights()

        #biases
        self.bI = [random.uniform(-1, 1) for _ in range(self.hidden_neurons)]
        self.bH = [random.uniform(-1, 1) for _ in range(self.outputs)]

    def init_weights(self):
        self.wI = [None] * self.inputs
        for row in range(self.inputs):
            self.wI[row] = [random.uniform(-1, 1) for _ in range(self.inputs)]

        self.wH = [None] * self.hidden_neurons
        for row in range(self.hidden_neurons):
            self.wH[row] = [random.uniform(-1, 1) for _ in range(self.hidden_neurons)]

    def forward_propagation(self, input_arr):
        hidden_arr = [None] * self.hidden_neurons

        for i in range(self.hidden_neurons):
            wSum = 0
            for j in range(self.inputs):
                wSum += self.wI[i][j] * input_arr[j] / c.SENSOR_RANGE
            wSum += self.bI[i]
            hidden_arr[i] = sigmoid(wSum)

        output_arr = [None] * self.outputs
        for i in range(self.outputs):
            wSum = 0
            for j in range(self.hidden_neurons):
                wSum += self.wH[i][j] * hidden_arr[j]
            wSum += self.bH[i]
            output_arr[i] = sigmoid(wSum)

        return output_arr

    def crossbreed(self, net2):
        new_wI = [[None] * self.inputs] * self.hidden_neurons

        for i in range(self.hidden_neurons):
            for j in range(self.inputs):
                new_wI[i][j] = random.choice([self.wI[i][j], net2.wI[i][j]])

        new_wH = [[None] * self.hidden_neurons] * self.outputs
    
        for i in range(self.outputs):
            for j in range(self.hidden_neurons): 
                new_wH[i][j] = random.choice([self.wH[i][j], net2.wH[i][j]])

        new_bI = [None] * self.hidden_neurons
        for i in range(self.hidden_neurons):
            new_bI[i] = random.choice([self.bI[i], net2.bI[i]])

        new_bH = [None] * self.outputs
        for i in range(self.outputs):
            new_bH[i] = random.choice([self.bH[i], net2.bH[i]])

        return {
            "wI": new_wI,
            "wH": new_wH,
            "bI": new_bI,
            "bH": new_bH
        }

    def mutate(self):
        for x in range(5):
            i = random.randint(0, self.hidden_neurons - 1)
            j = random.randint(0, self.inputs - 1)
            self.wI[i][j] = random.uniform(-1, 1)

        for x in range(5):
            i = random.randint(0, self.outputs - 1)
            j = random.randint(0, self.hidden_neurons - 1)
            self.wH[i][j] = random.uniform(-1, 1)

    def load_params(self, params):
        self.wI = params["wI"]
        self.wH = params["wH"]
        self.bI = params["bI"]
        self.bH = params["bH"]

    def get_params(self):
        return {
            "wI": self.wI, 
            "wH": self.wH,
            "bI": self.bI,
            "bH": self.bH
        }

    
            
                






