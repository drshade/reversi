from game import Reversi
import random
import time

if __name__ == "__main__":
    # Random play

    start = time.time()
    iterations = 100
    
    for iteration in range(iterations):
        game = Reversi()
        #print (game.draw())
        (complete, whitepoints, blackpoints, empty) = game.stats()
        while not complete:
            options = game.all_valid_placements()
            if len(options) == 0:
                game.skip()
            else:
                (chosenx, choseny) = options[random.randint(0, len(options) - 1)]
                game.place(chosenx, choseny)
            (complete, whitepoints, blackpoints, empty) = game.stats()
            #print (game.draw())
        #print ("White: %d, Black: %d (%d moves)"%(whitepoints, blackpoints, len(game._moves)))
        result = 'd'
        if whitepoints > blackpoints:
            result = 'w'
        if whitepoints < blackpoints:
            result = 'b'
        for (who, (x, y), board) in game._moves:
            #print ("  (winner was %s) %s played move -> x: %d, y: %d -> %s"%(result, who, x, y, board))
            pass
    
    end = time.time()
    print("Took %0.3fs to run %d iterations"%(end - start, iterations))