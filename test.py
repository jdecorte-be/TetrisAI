import torch
import torch.nn as nn
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from PIL import ImageGrab
import torch.nn.functional as F
from game import Game
import numpy as np
import cv2


#exemple de ce a quoi ça doit ressembler la matrce
states_data = [
    [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]]]

actions_data = [
    [0],
    [90],  # rotation, gauche, droite
    [-1],
    [1],  # rotation, gauche, droite
    [32] 
    
]

class TetrisDataset(Dataset):
    def __init__(self, states, actions):
        # Supprimez la dernière colonne des états pour ajuster la taille à 22*12
        self.states = torch.tensor(states, dtype=torch.float32).view(-1, 22 * 12)
        self.actions = torch.tensor(actions, dtype=torch.float32)

    def __len__(self):
        return len(self.states)

    def __getitem__(self, index):
        return self.states[index], self.actions[index]

    
class Net(nn.Module):
    def __init__(self, input, hidden, output):
        super(Net, self).__init__()
        self.layer1 = nn.Linear(input, hidden)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(hidden, output)

    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)

        x = F.softmax(x, dim=1)

        return x

input_size = 22 * 12 
output_size = 5
hidden_size = 400
batch_size = 1

#initialise de Net
net = Net(input_size, hidden_size, output_size)

alive = True

if torch.cuda.is_available():
    torch.cuda.manual_seed(123)
else:
    torch.manual_seed(123)

if torch.cuda.is_available():
    model = torch.load("{}/tetris".format("model"))
else:
    model = torch.load("{}/tetris".format("model"), map_location=lambda storage, loc: storage)

model.eval()

if(torch.cuda.is_available()):
    model.cuda()

while(alive):
    g = Game()
    
    screen = ImageGrab.grab()
    screen = np.array(screen)
    img = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    g.detectBoard(img)
    #initialise le dataSet
    #state a récup avec algo de récup screen
    tetris_data = TetrisDataset(states=g.board, actions=actions_data)
    dataloader = DataLoader(tetris_data, batch_size=batch_size, shuffle=True)

    torch().start()

    # for batch in dataloader:
        # states_batch, actions_batch = batch

        # # Appliquez le modèle avec les data (équivalent a faire forward())
        # #output_batch nous donne comme résultat les probabilité de clicker sur les différents event
        # output_batch = model(states_batch)
        # key = output_batch.argmax().item()
        
        # if key == 1:
        #     g.Player.up()
        # if key == 2:
        #     g.Player.left()
        # if key == 3:
        #     g.Player.right()
        # if key == 4:
        #     g.Player.space()
        #     # print(key.item())

