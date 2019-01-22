import random
from utils import sigmoid
import config as c

class NeuralNet():
    def __init__(self, inputs, hidden_neurons, outputs):
        self.inputs = inputs
        self.hidden_neurons = hidden_neurons
        self.outputs = outputs

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
            print(wSum)
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
                new_wI[i][j] = random.uniform(self.wI[i][j], net2.wI[i][j])

        new_wH = [[None] * self.hidden_neurons] * self.outputs
    
        for i in range(self.outputs):
            for j in range(self.hidden_neurons): 
                new_wH[i][j] = random.uniform(self.wH[i][j], net2.wH[i][j])

        return {"wI": new_wI, "wH": new_wH}

    def mutate(self):
        for x in range(5):
            i = random.randint(0, self.hidden_neurons - 1)
            j = random.randint(0, self.inputs - 1)
            self.wI[i][j] = random.uniform(-1, 1)

    def load_parameters(self, params):
        self.wI = params["wI"]
        self.wH = params["wH"]

    
            
                






